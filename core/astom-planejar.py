#!/usr/bin/env python3
"""ASTOM Platform — gerador de plano somente leitura."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSAO = "0.1.0-dev"
SCHEMA_SUPORTADO = 1


class ErroPlanejamento(Exception):
    """Erro esperado durante leitura, validação ou gravação do plano."""


@dataclass(frozen=True)
class ResultadoComponente:
    identificador: str
    categoria: str
    descricao: str
    obrigatorio: bool
    estado: str
    acao: str


def executar_consulta(comando: list[str]) -> str:
    """Executa uma consulta sem shell e devolve a primeira saída útil."""
    try:
        processo = subprocess.run(
            comando,
            check=False,
            capture_output=True,
            text=True,
            timeout=3,
            env=os.environ.copy(),
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return processo.stdout.strip()


def ler_os_release() -> dict[str, str]:
    dados: dict[str, str] = {}
    caminho = Path("/etc/os-release")
    if not caminho.is_file():
        return dados

    try:
        linhas = caminho.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return dados

    for linha in linhas:
        if "=" not in linha or linha.lstrip().startswith("#"):
            continue
        chave, valor = linha.split("=", 1)
        dados[chave] = valor.strip().strip('"')
    return dados


def carregar_manifesto(caminho: Path) -> dict[str, Any]:
    if not caminho.is_file():
        raise ErroPlanejamento(f"manifesto não encontrado: {caminho}")

    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except OSError as erro:
        raise ErroPlanejamento(f"falha ao ler o manifesto: {erro}") from erro
    except json.JSONDecodeError as erro:
        raise ErroPlanejamento(
            f"manifesto JSON inválido na linha {erro.lineno}, coluna {erro.colno}"
        ) from erro

    if not isinstance(dados, dict):
        raise ErroPlanejamento("a raiz do manifesto precisa ser um objeto JSON")

    if dados.get("schema_version") != SCHEMA_SUPORTADO:
        raise ErroPlanejamento(
            f"schema_version incompatível; esperado {SCHEMA_SUPORTADO}"
        )

    for campo in ("id", "title", "components"):
        if campo not in dados:
            raise ErroPlanejamento(f"campo obrigatório ausente no manifesto: {campo}")

    if not isinstance(dados["components"], list):
        raise ErroPlanejamento("components precisa ser uma lista")

    identificadores: set[str] = set()
    for indice, componente in enumerate(dados["components"], start=1):
        if not isinstance(componente, dict):
            raise ErroPlanejamento(f"componente {indice} precisa ser um objeto")
        for campo in ("id", "type", "description", "required"):
            if campo not in componente:
                raise ErroPlanejamento(
                    f"campo {campo} ausente no componente {indice}"
                )
        if componente["id"] in identificadores:
            raise ErroPlanejamento(
                f"identificador de componente duplicado: {componente['id']}"
            )
        identificadores.add(str(componente["id"]))
        if componente["type"] != "command":
            raise ErroPlanejamento(
                f"tipo de componente ainda não suportado: {componente['type']}"
            )
        if not isinstance(componente["required"], bool):
            raise ErroPlanejamento(
                f"required precisa ser booleano no componente {componente['id']}"
            )
        if not componente.get("command"):
            raise ErroPlanejamento(
                f"command ausente no componente {componente['id']}"
            )

    return dados


def avaliar_alvo(manifesto: dict[str, Any]) -> list[tuple[str, str, str]]:
    alvo = manifesto.get("target", {})
    if not isinstance(alvo, dict):
        raise ErroPlanejamento("target precisa ser um objeto")

    os_release = ler_os_release()
    distribuicao = os_release.get("ID", "não identificada").lower()
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "não identificado")
    sessao = os.environ.get("XDG_SESSION_TYPE", "não identificada").lower()
    fs_raiz = executar_consulta(["findmnt", "-n", "-o", "FSTYPE", "/"])

    resultados: list[tuple[str, str, str]] = []

    ids_aceitos = [str(item).lower() for item in alvo.get("distribution_ids", [])]
    estado_distribuicao = (
        "compatível" if not ids_aceitos or distribuicao in ids_aceitos else "fora do alvo"
    )
    resultados.append(("Distribuição", distribuicao, estado_distribuicao))

    desktops_aceitos = [str(item).lower() for item in alvo.get("desktop_contains", [])]
    desktop_compativel = not desktops_aceitos or any(
        trecho in desktop.lower() for trecho in desktops_aceitos
    )
    resultados.append(
        ("Desktop", desktop, "compatível" if desktop_compativel else "fora do alvo")
    )

    sessoes_aceitas = [str(item).lower() for item in alvo.get("session_types", [])]
    estado_sessao = (
        "compatível" if not sessoes_aceitas or sessao in sessoes_aceitas else "fora do alvo"
    )
    resultados.append(("Sessão", sessao, estado_sessao))

    sistemas_arquivos = [str(item).lower() for item in alvo.get("root_filesystems", [])]
    fs_normalizado = fs_raiz.lower() if fs_raiz else "não identificado"
    estado_fs = (
        "compatível"
        if not sistemas_arquivos or fs_normalizado in sistemas_arquivos
        else "fora do alvo"
    )
    resultados.append(("Sistema de arquivos raiz", fs_normalizado, estado_fs))

    return resultados


def avaliar_componentes(manifesto: dict[str, Any]) -> list[ResultadoComponente]:
    resultados: list[ResultadoComponente] = []
    for componente in manifesto["components"]:
        comando = str(componente["command"])
        detectado = shutil.which(comando) is not None
        obrigatorio = bool(componente["required"])

        if detectado:
            estado = "presente"
            acao = "nenhuma"
        elif obrigatorio:
            estado = "ausente"
            acao = str(
                componente.get(
                    "when_missing",
                    "revisar e instalar somente após confirmação explícita",
                )
            )
        else:
            estado = "opcional ausente"
            acao = str(componente.get("when_missing", "nenhuma"))

        resultados.append(
            ResultadoComponente(
                identificador=str(componente["id"]),
                categoria=str(componente.get("category", "geral")),
                descricao=str(componente["description"]),
                obrigatorio=obrigatorio,
                estado=estado,
                acao=acao,
            )
        )
    return resultados


def escapar_tabela(valor: object) -> str:
    return str(valor).replace("\n", " ").replace("|", "\\|")


def gerar_markdown(
    manifesto: dict[str, Any],
    caminho_manifesto: Path,
    alvo: list[tuple[str, str, str]],
    componentes: list[ResultadoComponente],
) -> str:
    presentes = sum(item.estado == "presente" for item in componentes)
    ausentes_obrigatorios = sum(item.estado == "ausente" for item in componentes)
    opcionais_ausentes = sum(item.estado == "opcional ausente" for item in componentes)

    linhas = [
        "# Plano de implantação ASTOM",
        "",
        f"- **Versão do planejador:** `{VERSAO}`",
        f"- **Perfil:** `{escapar_tabela(manifesto['id'])}`",
        f"- **Título:** {escapar_tabela(manifesto['title'])}",
        f"- **Manifesto:** `{escapar_tabela(caminho_manifesto)}`",
        f"- **Gerado em:** `{datetime.now(timezone.utc).isoformat()}`",
        "- **Modo:** somente leitura; nenhuma alteração foi executada",
        "",
        "## Compatibilidade do ambiente",
        "",
        "| Critério | Detectado | Avaliação |",
        "|---|---|---|",
    ]

    for criterio, detectado, estado in alvo:
        linhas.append(
            f"| {escapar_tabela(criterio)} | {escapar_tabela(detectado)} | {escapar_tabela(estado)} |"
        )

    linhas.extend(
        [
            "",
            "## Componentes",
            "",
            "| Componente | Categoria | Obrigatório | Estado | Ação proposta |",
            "|---|---|---:|---|---|",
        ]
    )

    for item in componentes:
        linhas.append(
            "| "
            + " | ".join(
                [
                    escapar_tabela(f"{item.identificador} — {item.descricao}"),
                    escapar_tabela(item.categoria),
                    "sim" if item.obrigatorio else "não",
                    escapar_tabela(item.estado),
                    escapar_tabela(item.acao),
                ]
            )
            + " |"
        )

    linhas.extend(
        [
            "",
            "## Resumo",
            "",
            f"- Componentes presentes: **{presentes}**",
            f"- Componentes obrigatórios ausentes: **{ausentes_obrigatorios}**",
            f"- Componentes opcionais ausentes: **{opcionais_ausentes}**",
            "",
            "## Garantias deste modo",
            "",
            "- nenhum pacote foi instalado ou removido;",
            "- nenhum serviço foi iniciado, interrompido ou habilitado;",
            "- nenhum arquivo de configuração do sistema foi alterado;",
            "- nenhuma ação proposta deve ser executada sem revisão e confirmação explícita.",
            "",
        ]
    )
    return "\n".join(linhas)


def gravar_atomicamente(destino: Path, conteudo: str) -> None:
    diretorio = destino.parent
    if not diretorio.is_dir():
        raise ErroPlanejamento(f"diretório de saída inexistente: {diretorio}")
    if not os.access(diretorio, os.W_OK):
        raise ErroPlanejamento(f"diretório de saída sem permissão de escrita: {diretorio}")

    temporario: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=diretorio,
            prefix=f".{destino.name}.",
            suffix=".tmp",
            delete=False,
        ) as arquivo:
            temporario = Path(arquivo.name)
            arquivo.write(conteudo)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, destino)
        temporario = None
    except OSError as erro:
        raise ErroPlanejamento(f"falha ao gravar o plano: {erro}") from erro
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera um plano ASTOM somente leitura a partir de um manifesto JSON."
    )
    parser.add_argument("--manifest", required=True, type=Path, help="manifesto JSON")
    parser.add_argument("--output", required=True, type=Path, help="plano Markdown")
    return parser.parse_args()


def main() -> int:
    opcoes = argumentos()
    try:
        manifesto = carregar_manifesto(opcoes.manifest)
        alvo = avaliar_alvo(manifesto)
        componentes = avaliar_componentes(manifesto)
        conteudo = gerar_markdown(manifesto, opcoes.manifest, alvo, componentes)
        gravar_atomicamente(opcoes.output, conteudo)
    except ErroPlanejamento as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    print(f"Plano criado: {opcoes.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
