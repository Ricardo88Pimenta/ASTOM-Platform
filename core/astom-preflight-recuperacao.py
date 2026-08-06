#!/usr/bin/env python3
"""ASTOM Platform — pré-flight somente leitura para backup e Snapper."""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

VERSAO = "0.1.0-dev"


class ErroPreflight(Exception):
    """Erro esperado durante consulta ou gravação do pré-flight."""


@dataclass(frozen=True)
class Verificacao:
    id: str
    descricao: str
    detectado: str
    estado: str
    bloqueante: bool


def executar(comando: list[str]) -> tuple[int, str]:
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


def consultar_configuracoes_snapper() -> tuple[str, list[tuple[str, str]]]:
    if shutil.which("snapper") is None:
        return "indisponível", []

    retorno, saida = executar(
        [
            "snapper",
            "--csvout",
            "--no-headers",
            "list-configs",
            "--columns",
            "config,subvolume",
        ]
    )
    if retorno != 0:
        return "falha na consulta", []
    if not saida:
        return "nenhuma configuração", []

    configuracoes: list[tuple[str, str]] = []
    try:
        for linha in csv.reader(io.StringIO(saida)):
            if len(linha) < 2:
                return "saída não reconhecida", []
            configuracoes.append((linha[0].strip(), linha[1].strip()))
    except csv.Error:
        return "saída não reconhecida", []
    return "consultado", configuracoes


def coletar_verificacoes() -> tuple[list[Verificacao], list[tuple[str, str]]]:
    _, fs_raiz = executar(["findmnt", "-n", "-o", "FSTYPE", "/"])
    fs_raiz = fs_raiz.lower() if fs_raiz else "não identificado"

    _, fonte_raiz = executar(["findmnt", "-n", "-o", "SOURCE", "/"])
    fonte_raiz = fonte_raiz or "não identificada"

    btrfs_disponivel = shutil.which("btrfs") is not None
    snapper_disponivel = shutil.which("snapper") is not None
    status_configs, configuracoes = consultar_configuracoes_snapper()
    config_raiz = next((nome for nome, subvolume in configuracoes if subvolume == "/"), "")

    verificacoes = [
        Verificacao(
            id="root-filesystem",
            descricao="Sistema de arquivos da raiz",
            detectado=fs_raiz,
            estado="aprovado" if fs_raiz == "btrfs" else "bloqueado",
            bloqueante=True,
        ),
        Verificacao(
            id="root-source",
            descricao="Origem do ponto de montagem raiz",
            detectado=fonte_raiz,
            estado="informativo",
            bloqueante=False,
        ),
        Verificacao(
            id="btrfs-cli",
            descricao="Ferramenta btrfs disponível",
            detectado="disponível" if btrfs_disponivel else "indisponível",
            estado="aprovado" if btrfs_disponivel else "bloqueado",
            bloqueante=True,
        ),
        Verificacao(
            id="snapper-cli",
            descricao="Ferramenta Snapper disponível",
            detectado="disponível" if snapper_disponivel else "indisponível",
            estado="aprovado" if snapper_disponivel else "bloqueado",
            bloqueante=True,
        ),
        Verificacao(
            id="snapper-config-query",
            descricao="Consulta de configurações Snapper",
            detectado=status_configs,
            estado="aprovado" if status_configs == "consultado" else "bloqueado",
            bloqueante=True,
        ),
        Verificacao(
            id="snapper-root-config",
            descricao="Configuração Snapper associada à raiz",
            detectado=config_raiz or "não encontrada",
            estado="aprovado" if config_raiz else "bloqueado",
            bloqueante=True,
        ),
    ]
    return verificacoes, configuracoes


def resultado_gate(verificacoes: list[Verificacao]) -> str:
    return (
        "apto para teste controlado de snapshot"
        if all(v.estado != "bloqueado" for v in verificacoes if v.bloqueante)
        else "bloqueado para criação de snapshot"
    )


def escapar(valor: object) -> str:
    return str(valor).replace("\n", " ").replace("|", "\\|")


def gerar_markdown(
    verificacoes: list[Verificacao], configuracoes: list[tuple[str, str]]
) -> str:
    gate = resultado_gate(verificacoes)
    linhas = [
        "# Pré-flight de recuperação ASTOM",
        "",
        f"- **Versão:** `{VERSAO}`",
        f"- **Gerado em:** `{datetime.now(timezone.utc).isoformat()}`",
        "- **Modo:** somente leitura; nenhum snapshot ou backup foi criado",
        f"- **Gate:** **{gate}**",
        "",
        "## Verificações",
        "",
        "| Verificação | Detectado | Estado | Bloqueante |",
        "|---|---|---|---:|",
    ]
    for item in verificacoes:
        linhas.append(
            f"| {escapar(item.descricao)} | {escapar(item.detectado)} | "
            f"{escapar(item.estado)} | {'sim' if item.bloqueante else 'não'} |"
        )

    linhas.extend(["", "## Configurações Snapper detectadas", ""])
    if configuracoes:
        linhas.extend(["| Configuração | Subvolume |", "|---|---|"])
        for nome, subvolume in configuracoes:
            linhas.append(f"| {escapar(nome)} | {escapar(subvolume)} |")
    else:
        linhas.append("Nenhuma configuração utilizável foi confirmada.")

    linhas.extend(
        [
            "",
            "## Garantias",
            "",
            "- não utiliza `sudo`;",
            "- não executa `snapper create`, `delete` ou `rollback`;",
            "- não altera configurações do Snapper ou do Btrfs;",
            "- não cria cópias de arquivos;",
            "- apenas consulta capacidades necessárias à futura Fase 2.",
            "",
        ]
    )
    return "\n".join(linhas)


def gerar_json(
    verificacoes: list[Verificacao], configuracoes: list[tuple[str, str]]
) -> str:
    dados = {
        "astom_version": VERSAO,
        "mode": "read-only",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gate": resultado_gate(verificacoes),
        "checks": [asdict(item) for item in verificacoes],
        "snapper_configs": [
            {"config": nome, "subvolume": subvolume}
            for nome, subvolume in configuracoes
        ],
    }
    return json.dumps(dados, ensure_ascii=False, indent=2) + "\n"


def gravar_atomicamente(destino: Path, conteudo: str) -> None:
    diretorio = destino.parent
    if not diretorio.is_dir():
        raise ErroPreflight(f"diretório de saída inexistente: {diretorio}")
    if not os.access(diretorio, os.W_OK):
        raise ErroPreflight(f"diretório de saída sem permissão de escrita: {diretorio}")

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
        raise ErroPreflight(f"falha ao gravar a saída: {erro}") from erro
    finally:
        if temporario is not None:
            temporario.unlink(missing_ok=True)


def argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Avalia, sem alterações, a prontidão para backup e Snapper."
    )
    parser.add_argument("--output", required=True, type=Path, help="relatório Markdown")
    parser.add_argument("--json-output", type=Path, help="relatório JSON opcional")
    return parser.parse_args()


def main() -> int:
    opcoes = argumentos()
    try:
        verificacoes, configuracoes = coletar_verificacoes()
        gravar_atomicamente(opcoes.output, gerar_markdown(verificacoes, configuracoes))
        if opcoes.json_output is not None:
            gravar_atomicamente(
                opcoes.json_output, gerar_json(verificacoes, configuracoes)
            )
    except ErroPreflight as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    print(f"Pré-flight criado: {opcoes.output}")
    if opcoes.json_output is not None:
        print(f"Pré-flight JSON criado: {opcoes.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
