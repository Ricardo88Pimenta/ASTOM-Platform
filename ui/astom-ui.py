#!/usr/bin/env python3
"""ASTOM Platform — servidor local somente leitura para o protótipo de interface."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import subprocess
import sys
import tempfile
import threading
import webbrowser
from datetime import datetime, timezone
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

VERSAO = "0.2.0-dev"
SCHEMA_INTERFACE = 1
HOSTS_LOCAIS = {"127.0.0.1", "localhost", "::1"}


class ErroInterface(Exception):
    """Falha esperada ao preparar dados ou iniciar a interface."""


def ler_json(caminho: Path) -> dict[str, Any]:
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except OSError as erro:
        raise ErroInterface(f"falha ao ler JSON: {caminho}: {erro}") from erro
    except json.JSONDecodeError as erro:
        raise ErroInterface(
            f"JSON inválido em {caminho}, linha {erro.lineno}, coluna {erro.colno}"
        ) from erro
    if not isinstance(dados, dict):
        raise ErroInterface(f"a raiz de {caminho} precisa ser um objeto JSON")
    return dados


def executar_coletor(
    script: Path,
    argumentos: list[str],
    raiz_repositorio: Path,
    timeout: int = 20,
) -> None:
    if not script.is_file():
        raise ErroInterface(f"coletor não encontrado: {script}")
    try:
        processo = subprocess.run(
            [sys.executable, str(script), *argumentos],
            cwd=raiz_repositorio,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=os.environ.copy(),
        )
    except (OSError, subprocess.SubprocessError) as erro:
        raise ErroInterface(f"falha ao executar {script.name}: {erro}") from erro
    if processo.returncode != 0:
        detalhe = (processo.stderr or processo.stdout).strip().splitlines()
        mensagem = detalhe[-1] if detalhe else "erro sem detalhes"
        raise ErroInterface(f"{script.name} falhou: {mensagem[:240]}")


def validar_estado(dados: dict[str, Any]) -> None:
    campos = ("schema_version", "mode", "source", "generated_at", "planner", "recovery")
    ausentes = [campo for campo in campos if campo not in dados]
    if ausentes:
        raise ErroInterface(f"estado da interface incompleto: {', '.join(ausentes)}")
    if dados["schema_version"] != SCHEMA_INTERFACE:
        raise ErroInterface(
            f"schema da interface incompatível: {dados['schema_version']}"
        )
    if dados["mode"] != "read-only":
        raise ErroInterface("a interface de teste aceita apenas modo read-only")
    if not isinstance(dados["planner"], dict) or not isinstance(dados["recovery"], dict):
        raise ErroInterface("planner e recovery precisam ser objetos JSON")


def coletar_estado(raiz_repositorio: Path, manifesto: Path) -> dict[str, Any]:
    """Executa os coletores somente leitura e combina suas saídas."""
    raiz_repositorio = raiz_repositorio.resolve()
    manifesto = manifesto.resolve()
    planejador = raiz_repositorio / "core" / "astom-planejar.py"
    preflight = raiz_repositorio / "core" / "astom-preflight-recuperacao.py"

    if not manifesto.is_file():
        raise ErroInterface(f"manifesto não encontrado: {manifesto}")

    with tempfile.TemporaryDirectory(prefix="astom-ui-") as temporario:
        pasta = Path(temporario)
        plano_md = pasta / "plano.md"
        plano_json = pasta / "plano.json"
        preflight_md = pasta / "preflight.md"
        preflight_json = pasta / "preflight.json"

        executar_coletor(
            planejador,
            [
                "--manifest",
                str(manifesto),
                "--output",
                str(plano_md),
                "--json-output",
                str(plano_json),
            ],
            raiz_repositorio,
        )
        executar_coletor(
            preflight,
            [
                "--output",
                str(preflight_md),
                "--json-output",
                str(preflight_json),
            ],
            raiz_repositorio,
        )

        estado = {
            "schema_version": SCHEMA_INTERFACE,
            "astom_version": VERSAO,
            "mode": "read-only",
            "source": "live",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "homologation": {
                "current": "H1",
                "next": "H2",
                "interface": "P1",
                "message": "Protótipo funcional para avaliação de experiência e leitura de dados reais.",
            },
            "planner": ler_json(plano_json),
            "recovery": ler_json(preflight_json),
        }
    validar_estado(estado)
    return estado


def provedor_fixture(caminho: Path) -> Callable[[], dict[str, Any]]:
    caminho = caminho.resolve()

    def carregar() -> dict[str, Any]:
        dados = ler_json(caminho)
        validar_estado(dados)
        return dados

    return carregar


def provedor_live(raiz: Path, manifesto: Path) -> Callable[[], dict[str, Any]]:
    return lambda: coletar_estado(raiz, manifesto)


class ManipuladorASTOM(SimpleHTTPRequestHandler):
    """Serve arquivos locais e uma API somente leitura."""

    server_version = "ASTOMInterface/0.2"

    def __init__(
        self,
        *args: Any,
        directory: str,
        state_provider: Callable[[], dict[str, Any]],
        **kwargs: Any,
    ) -> None:
        self.state_provider = state_provider
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, formato: str, *args: Any) -> None:
        sys.stderr.write("[ASTOM UI] " + (formato % args) + "\n")

    def end_headers(self) -> None:
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
        )
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        super().end_headers()

    def enviar_json(self, status: HTTPStatus, dados: dict[str, Any]) -> None:
        corpo = (json.dumps(dados, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self) -> None:  # noqa: N802
        rota = urlparse(self.path).path
        if rota == "/api/health":
            self.enviar_json(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "version": VERSAO,
                    "mode": "read-only",
                },
            )
            return
        if rota == "/api/state":
            try:
                dados = self.state_provider()
                validar_estado(dados)
            except ErroInterface as erro:
                self.enviar_json(
                    HTTPStatus.SERVICE_UNAVAILABLE,
                    {
                        "status": "error",
                        "mode": "read-only",
                        "message": str(erro),
                    },
                )
                return
            self.enviar_json(HTTPStatus.OK, dados)
            return
        if rota == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        self.enviar_json(
            HTTPStatus.METHOD_NOT_ALLOWED,
            {
                "status": "error",
                "message": "a interface de teste não aceita operações mutáveis",
            },
        )

    do_PUT = do_POST  # type: ignore[assignment]
    do_DELETE = do_POST  # type: ignore[assignment]
    do_PATCH = do_POST  # type: ignore[assignment]


def criar_servidor(
    host: str,
    porta: int,
    pasta_estatica: Path,
    state_provider: Callable[[], dict[str, Any]],
) -> ThreadingHTTPServer:
    if not pasta_estatica.is_dir():
        raise ErroInterface(f"interface estática não encontrada: {pasta_estatica}")
    mimetypes.add_type("text/javascript", ".js")
    manipulador = partial(
        ManipuladorASTOM,
        directory=str(pasta_estatica.resolve()),
        state_provider=state_provider,
    )
    servidor = ThreadingHTTPServer((host, porta), manipulador)
    servidor.daemon_threads = True
    return servidor


def argumentos() -> argparse.Namespace:
    caminho = Path(__file__).resolve()
    raiz = caminho.parent.parent
    parser = argparse.ArgumentParser(
        description="Inicia o protótipo local da interface ASTOM em modo somente leitura."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--allow-remote", action="store_true")
    parser.add_argument("--open", action="store_true", dest="abrir")
    parser.add_argument("--repo-root", type=Path, default=raiz)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=raiz / "profiles" / "cachyos-kde-wayland-base.json",
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        help="usa um estado JSON de demonstração em vez dos coletores reais",
    )
    return parser.parse_args()


def main() -> int:
    opcoes = argumentos()
    if opcoes.host not in HOSTS_LOCAIS and not opcoes.allow_remote:
        print(
            "Erro: host remoto bloqueado; use --allow-remote somente em ambiente confiável.",
            file=sys.stderr,
        )
        return 2

    caminho = Path(__file__).resolve()
    pasta_estatica = caminho.parent / "control-center"
    provedor = (
        provedor_fixture(opcoes.fixture)
        if opcoes.fixture is not None
        else provedor_live(opcoes.repo_root, opcoes.manifest)
    )

    try:
        servidor = criar_servidor(opcoes.host, opcoes.port, pasta_estatica, provedor)
    except (ErroInterface, OSError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    host_exibido = "127.0.0.1" if opcoes.host in {"0.0.0.0", "::"} else opcoes.host
    url = f"http://{host_exibido}:{servidor.server_port}/"
    print(f"ASTOM Interface disponível em {url}")
    print("Modo somente leitura. Pressione Ctrl+C para encerrar.")

    if opcoes.abrir:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()

    try:
        servidor.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        print("\nEncerrando ASTOM Interface.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
