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
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSAO = "0.1.0-dev"
SCHEMA_SUPORTADO = 1
TIPOS_SUPORTADOS = {"command", "package", "flatpak"}
GERENCIADORES_SUPORTADOS = {"pacman", "apt", "dnf", "zypper"}


class ErroPlanejamento(Exception):
    """Erro esperado durante leitura, validação ou gravação do plano."""


@dataclass(frozen=True)
class ResultadoComponente:
    identificador: str
    tipo: str
    categoria: str
    descricao: str
    obrigatorio: bool
    estado: str
    versao: str
    fonte: str
    acao: str


def executar_consulta(comando: list[str]) -> tuple[int, str]:
    """Executa uma consulta sem shell, com timeout e sem elevar privilégios."""
    try:
        processo = subprocess.run(
            comando,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
            env=os.environ.copy(),
        )
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return processo.returncode, processo.stdout.strip()


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


def exigir_texto(componente: dict[str, Any], campo: str, indice: int) -> str:
    valor = componente.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise ErroPlanejamento(
            f"{campo} precisa ser texto não vazio no componente {indice}"
        )
    return valor.strip()


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

    if not isinstance(dados["id"], str) or not dados["id"].strip():
        raise ErroPlanejamento("id do manifesto precisa ser texto não vazio")
    if not isinstance(dados["title"], str) or not dados["title"].strip():
        raise ErroPlanejamento("title do manifesto precisa ser texto não vazio")
    if not isinstance(dados["components"], list):
        raise ErroPlanejamento("components precisa ser uma lista")

    identificadores: set[str] = set()
    for indice, componente in enumerate(dados["components"], start=1):
        if not isinstance(componente, dict):
            raise ErroPlanejamento(f"componente {indice} precisa ser um objeto")

        identificador = exigir_texto(componente, "id", indice)
        exigir_texto(componente, "description", indice)
        tipo = exigir_texto(componente, "type", indice)

        if identificador in identificadores:
            raise ErroPlanejamento(
                f"identificador de componente duplicado: {identificador}"
            )
        identificadores.add(identificador)

        if tipo not in TIPOS_SUPORTADOS:
            raise ErroPlanejamento(f"tipo de componente não suportado: {tipo}")
        if not isinstance(componente.get("required"), bool):
            raise ErroPlanejamento(
                f"required precisa ser booleano no componente {identificador}"
            )

        if tipo == "command":
            exigir_texto(componente, "command", indice)
        elif tipo == "package":
            exigir_texto(componente, "package", indice)
            gerenciador = exigir_texto(componente, "manager", indice)
            if gerenciador not in GERENCIADORES_SUPORTADOS:
                raise ErroPlanejamento(
                    f"gerenciador não suportado no componente {identificador}: {gerenciador}"
                )
        elif tipo == "flatpak":
            exigir_texto(componente, "app_id", indice)

        versao = componente.get("version")
        if versao is not None and (not isinstance(versao, str) or not versao.strip()):
            raise ErroPlanejamento(
                f"version precisa ser texto não vazio no componente {identificador}"
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
    _, fs_raiz = executar_consulta(["findmnt", "-n", "-o", "FSTYPE", "/"])

    resultados: list[tuple[str, str, str]] = []

    ids_aceitos = [str(item).lower() for item in alvo.get("distribution_ids", [])]
    resultados.append(
        (
            "Distribuição",
            distribuicao,
            "compatível" if not ids_aceitos or distribuicao in ids_aceitos else "fora do alvo",
        )
    )

    desktops_aceitos = [str(item).lower() for item in alvo.get("desktop_contains", [])]
    desktop_compativel = not desktops_aceitos or any(
        trecho in desktop.lower() for trecho in desktops_aceitos
    )
    resultados.append(
        ("Desktop", desktop, "compatível" if desktop_compativel else "fora do alvo")
    )

    sessoes_aceitas = [str(item).lower() for item in alvo.get("session_types", [])]
    resultados.append(
        (
            "Sessão",
            sessao,
            "compatível" if not sessoes_aceitas or sessao in sessoes_aceitas else "fora do alvo",
        )
    )

    sistemas_arquivos = [str(item).lower() for item in alvo.get("root_filesystems", [])]
    fs_normalizado = fs_raiz.lower() if fs_raiz else "não identificado"
    resultados.append(
        (
            "Sistema de arquivos raiz",
            fs_normalizado,
            "compatível"
            if not sistemas_arquivos or fs_normalizado in sistemas_arquivos
            else "fora do alvo",
        )
    )

    return resultados


def detectar_pacote(gerenciador: str, pacote: str) -> tuple[str, str, str]:
    """Retorna estado, versão e fonte para uma consulta de pacote."""
    if gerenciador == "pacman":
        if shutil.which("pacman") is None:
            return "detector indisponível", "não identificada", "pacman"
        retorno, saida = executar_consulta(["pacman", "-Q", pacote])
        if retorno == 0 and saida:
            partes = saida.split(maxsplit=1)
            versao = partes[1] if len(partes) == 2 else "não identificada"
            return "presente", versao, "pacman"
        return "ausente", "não instalada", "pacman"

    if gerenciador == "apt":
        if shutil.which("dpkg-query") is None:
            return "detector indisponível", "não identificada", "dpkg-query"
        retorno, saida = executar_consulta(
            ["dpkg-query", "-W", "-f=${Status}\t${Version}", pacote]
        )
        if retorno == 0 and saida.startswith("install ok installed\t"):
            return "presente", saida.split("\t", 1)[1], "dpkg-query"
        return "ausente", "não instalada", "dpkg-query"

    if gerenciador in {"dnf", "zypper"}:
        if shutil.which(gerenciador) is None or shutil.which("rpm") is None:
            return "detector indisponível", "não identificada", f"{gerenciador}/rpm"
        retorno, saida = executar_consulta(
            ["rpm", "-q", "--qf", "%{VERSION}-%{RELEASE}", pacote]
        )
        if retorno == 0 and saida:
            return "presente", saida, f"{gerenciador}/rpm"
        return "ausente", "não instalada", f"{gerenciador}/rpm"

    return "detector indisponível", "não identificada", gerenciador


def detectar_flatpak(app_id: str) -> tuple[str, str, str]:
    if shutil.which("flatpak") is None:
        return "detector indisponível", "não identificada", "flatpak"
    retorno, saida = executar_consulta(["flatpak", "info", "--show-version", app_id])
    if retorno == 0:
        return "presente", saida or "não identificada", "flatpak"
    return "ausente", "não instalada", "flatpak"


def acao_para_estado(componente: dict[str, Any], estado: str) -> str:
    obrigatorio = bool(componente["required"])
    if estado == "presente":
        return "nenhuma"
    if estado == "versão divergente":
        return str(
            componente.get(
                "when_version_mismatch",
                "revisar versão antes de qualquer alteração",
            )
        )
    if estado == "detector indisponível":
        return str(
            componente.get(
                "when_detector_unavailable",
                "revisar compatibilidade e disponibilidade do detector",
            )
        )
    if obrigatorio:
        return str(
            componente.get(
                "when_missing",
                "revisar e instalar somente após confirmação explícita",
            )
        )
    return str(componente.get("when_missing", "nenhuma"))


def avaliar_componentes(manifesto: dict[str, Any]) -> list[ResultadoComponente]:
    resultados: list[ResultadoComponente] = []

    for componente in manifesto["components"]:
        tipo = str(componente["type"])
        versao = "não aplicável"
        fonte = tipo

        if tipo == "command":
            comando = str(componente["command"])
            estado = "presente" if shutil.which(comando) is not None else "ausente"
            fonte = "PATH"
        elif tipo == "package":
            estado, versao, fonte = detectar_pacote(
                str(componente["manager"]), str(componente["package"])
            )
        else:
            estado, versao, fonte = detectar_flatpak(str(componente["app_id"]))

        versao_esperada = componente.get("version")
        if estado == "presente" and versao_esperada and versao != versao_esperada:
            estado = "versão divergente"

        obrigatorio = bool(componente["required"])
        estado_exibido = estado
        if estado == "ausente" and not obrigatorio:
            estado_exibido = "opcional ausente"

        resultados.append(
            ResultadoComponente(
                identificador=str(componente["id"]),
                tipo=tipo,
                categoria=str(componente.get("category", "geral")),
                descricao=str(componente["description"]),
                obrigatorio=obrigatorio,
                estado=estado_exibido,
                versao=versao,
                fonte=fonte,
                acao=acao_para_estado(componente, estado),
            )
        )

    return resultados


def escapar_tabela(valor: object) -> str:
    return str(valor).replace("\n", " ").replace("|", "\\|")


def resumo_componentes(componentes: list[ResultadoComponente]) -> dict[str, int]:
    return {
        "presentes": sum(item.estado == "presente" for item in componentes),
        "ausentes_obrigatorios": sum(item.estado == "ausente" for item in componentes),
        "opcionais_ausentes": sum(
            item.estado == "opcional ausente" for item in componentes
        ),
        "versoes_divergentes": sum(
            item.estado == "versão divergente" for item in componentes
        ),
        "detectores_indisponiveis": sum(
            item.estado == "detector indisponível" for item in componentes
        ),
    }


def gerar_markdown(
    manifesto: dict[str, Any],
    caminho_manifesto: Path,
    alvo: list[tuple[str, str, str]],
    componentes: list[ResultadoComponente],
) -> str:
    resumo = resumo_componentes(componentes)
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
            "| Componente | Tipo | Categoria | Obrigatório | Estado | Versão | Fonte | Ação proposta |",
            "|---|---|---|---:|---|---|---|---|",
        ]
    )

    for item in componentes:
        linhas.append(
            "| "
            + " | ".join(
                [
                    escapar_tabela(f"{item.identificador} — {item.descricao}"),
                    escapar_tabela(item.tipo),
                    escapar_tabela(item.categoria),
                    "sim" if item.obrigatorio else "não",
                    escapar_tabela(item.estado),
                    escapar_tabela(item.versao),
                    escapar_tabela(item.fonte),
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
            f"- Componentes presentes: **{resumo['presentes']}**",
            f"- Componentes obrigatórios ausentes: **{resumo['ausentes_obrigatorios']}**",
            f"- Componentes opcionais ausentes: **{resumo['opcionais_ausentes']}**",
            f"- Versões divergentes: **{resumo['versoes_divergentes']}**",
            f"- Detectores indisponíveis: **{resumo['detectores_indisponiveis']}**",
            "",
            "## Garantias deste modo",
            "",
            "- nenhum pacote foi instalado ou removido;",
            "- nenhum serviço foi iniciado, interrompido ou habilitado;",
            "- nenhum arquivo de configuração do sistema foi alterado;",
            "- consultas de pacotes e Flatpaks são executadas sem shell e sem sudo;",
            "- nenhuma ação proposta deve ser executada sem revisão e confirmação explícita.",
            "",
        ]
    )
    return "\n".join(linhas)


def gerar_json(
    manifesto: dict[str, Any],
    caminho_manifesto: Path,
    alvo: list[tuple[str, str, str]],
    componentes: list[ResultadoComponente],
) -> str:
    dados = {
        "astom_version": VERSAO,
        "mode": "read-only",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "profile": {
            "id": manifesto["id"],
            "title": manifesto["title"],
            "manifest": str(caminho_manifesto),
        },
        "target": [
            {"criterion": criterio, "detected": detectado, "status": estado}
            for criterio, detectado, estado in alvo
        ],
        "components": [asdict(item) for item in componentes],
        "summary": resumo_componentes(componentes),
    }
    return json.dumps(dados, ensure_ascii=False, indent=2) + "\n"


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
        raise ErroPlanejamento(f"falha ao gravar a saída: {erro}") from erro
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera um plano ASTOM somente leitura a partir de um manifesto JSON."
    )
    parser.add_argument("--manifest", required=True, type=Path, help="manifesto JSON")
    parser.add_argument("--output", required=True, type=Path, help="plano Markdown")
    parser.add_argument(
        "--json-output",
        type=Path,
        help="saída JSON estruturada opcional, também gravada atomicamente",
    )
    return parser.parse_args()


def main() -> int:
    opcoes = argumentos()
    try:
        manifesto = carregar_manifesto(opcoes.manifest)
        alvo = avaliar_alvo(manifesto)
        componentes = avaliar_componentes(manifesto)
        gravar_atomicamente(
            opcoes.output,
            gerar_markdown(manifesto, opcoes.manifest, alvo, componentes),
        )
        if opcoes.json_output is not None:
            gravar_atomicamente(
                opcoes.json_output,
                gerar_json(manifesto, opcoes.manifest, alvo, componentes),
            )
    except ErroPlanejamento as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    print(f"Plano criado: {opcoes.output}")
    if opcoes.json_output is not None:
        print(f"Inventário JSON criado: {opcoes.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
