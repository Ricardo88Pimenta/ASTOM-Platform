#!/usr/bin/env bash

# ASTOM Platform — Diagnóstico somente leitura
# Versão: 0.1.0-dev
# Este script não instala, remove ou altera configurações do sistema.

set -uo pipefail

VERSAO="0.1.0-dev"
DATA="$(date '+%Y-%m-%d_%H-%M-%S')"
SAIDA="${1:-astom-diagnostico-${DATA}.md}"

sanitizar() {
    local valor="${1:-não disponível}"
    valor="${valor//$'\n'/ }"
    valor="${valor//|/\\|}"
    printf '%s' "$valor"
}

linha() {
    local nome="$1"
    local valor="${2:-não disponível}"
    printf '| %s | %s |\n' "$nome" "$(sanitizar "$valor")"
}

existe() {
    command -v "$1" >/dev/null 2>&1
}

estado_servico_usuario() {
    local servico="$1"
    if ! existe systemctl; then
        printf 'systemctl indisponível'
        return
    fi

    systemctl --user is-active "$servico" 2>/dev/null || printf 'inativo ou indisponível'
}

estado_servico_sistema() {
    local servico="$1"
    if ! existe systemctl; then
        printf 'systemctl indisponível'
        return
    fi

    systemctl is-active "$servico" 2>/dev/null || printf 'inativo ou indisponível'
}

valor_seguro() {
    "$@" 2>/dev/null || true
}

gerar_relatorio() {
    printf '# Relatório de diagnóstico ASTOM\n\n'
    printf -- '- **Versão do diagnóstico:** `%s`\n' "$VERSAO"
    printf -- '- **Data:** `%s`\n' "$(date --iso-8601=seconds 2>/dev/null || date)"
    printf -- '- **Modo:** somente leitura\n\n'

    printf '## Sistema\n\n'
    printf '| Item | Resultado |\n'
    printf '|---|---|\n'
    linha 'Distribuição' "$DISTRIBUICAO"
    linha 'Kernel' "$KERNEL"
    linha 'Arquitetura' "$ARQUITETURA"
    linha 'Desktop' "$DESKTOP"
    linha 'Sessão gráfica' "$SESSAO"
    linha 'Shell' "$SHELL_ATUAL"
    linha 'Gerenciadores detectados' "$GERENCIADOR"

    printf '\n## Armazenamento, boot e recuperação\n\n'
    printf '| Item | Resultado |\n'
    printf '|---|---|\n'
    linha 'Sistema de arquivos da raiz' "$FS_RAIZ"
    linha 'Opções de montagem da raiz' "$OPCOES_RAIZ"
    linha 'Snapper' "$SNAPPER"
    linha 'Boot' "$BOOT"
    linha 'TRIM periódico' "$(estado_servico_sistema fstrim.timer)"

    printf '\n## Gráficos e sessão\n\n'
    printf '| Item | Resultado |\n'
    printf '|---|---|\n'
    linha 'GPU' "$GPU"
    linha 'Driver NVIDIA' "$DRIVER_NVIDIA"
    linha 'Wayland' "$([[ "$SESSAO" == "wayland" ]] && printf 'ativo' || printf 'não confirmado')"

    printf '\n## Áudio, memória e segurança\n\n'
    printf '| Item | Resultado |\n'
    printf '|---|---|\n'
    linha 'PipeWire' "$(estado_servico_usuario pipewire.service)"
    linha 'WirePlumber' "$(estado_servico_usuario wireplumber.service)"
    linha 'zRAM' "$(valor_seguro swapon --show --noheadings --output NAME | grep -q zram && printf 'ativa' || printf 'não confirmada')"
    linha 'UFW' "$UFW"

    printf '\n## Componentes detectados\n\n'
    printf '| Componente | Estado |\n'
    printf '|---|---|\n'
    for componente in "${COMPONENTES[@]}"; do
        if existe "$componente"; then
            linha "$componente" 'disponível no PATH'
        else
            linha "$componente" 'não detectado no PATH'
        fi
    done

    printf '\n## Observações\n\n'
    printf -- '- O relatório não contém endereços IP, números de série ou conteúdo de arquivos pessoais.\n'
    printf -- '- Ausência no `PATH` não prova que um aplicativo gráfico não esteja instalado.\n'
    printf -- '- Nenhuma alteração de sistema foi executada.\n'
    printf -- '- Resultados devem ser revisados antes de qualquer decisão de implantação.\n'
}

if [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    source /etc/os-release
fi

DISTRIBUICAO="${PRETTY_NAME:-${NAME:-não identificada}}"
KERNEL="$(uname -sr 2>/dev/null || true)"
ARQUITETURA="$(uname -m 2>/dev/null || true)"
SESSAO="${XDG_SESSION_TYPE:-não identificada}"
DESKTOP="${XDG_CURRENT_DESKTOP:-não identificado}"
SHELL_ATUAL="${SHELL:-não identificada}"
FS_RAIZ="$(valor_seguro findmnt -n -o FSTYPE /)"
OPCOES_RAIZ="$(valor_seguro findmnt -n -o OPTIONS /)"

GERENCIADOR="não identificado"
for candidato in pacman apt dnf zypper rpm-ostree flatpak; do
    if existe "$candidato"; then
        if [[ "$GERENCIADOR" == "não identificado" ]]; then
            GERENCIADOR="$candidato"
        else
            GERENCIADOR+="; $candidato"
        fi
    fi
done

GPU="não identificada"
DRIVER_NVIDIA="não detectado"
if existe nvidia-smi; then
    GPU="$(valor_seguro nvidia-smi --query-gpu=name --format=csv,noheader | paste -sd ';' -)"
    DRIVER_NVIDIA="$(valor_seguro nvidia-smi --query-gpu=driver_version --format=csv,noheader | paste -sd ';' -)"
elif existe lspci; then
    GPU="$(valor_seguro lspci | grep -Ei 'VGA|3D|Display' | sed 's/^[^ ]* //' | paste -sd ';' -)"
fi

SNAPPER="não instalado"
if existe snapper; then
    SNAPPER="instalado"
fi

BOOT="não identificado"
if existe bootctl; then
    if bootctl is-installed >/dev/null 2>&1; then
        BOOT="systemd-boot instalado"
    else
        BOOT="bootctl disponível; systemd-boot não confirmado"
    fi
fi

UFW="não instalado"
if existe ufw; then
    UFW="$(estado_servico_sistema ufw.service)"
fi

COMPONENTES=(
    steam
    heroic
    heroic-games-launcher
    lutris
    wine
    mangohud
    gamemoderun
    gamescope
    goverlay
    flatpak
    git
    kwin_wayland
    kvantummanager
    nextcloud
    bitwarden
)

DIRETORIO_SAIDA="$(dirname -- "$SAIDA")"

if [[ ! -d "$DIRETORIO_SAIDA" ]]; then
    printf 'Erro: diretório de saída inexistente: %s\n' "$DIRETORIO_SAIDA" >&2
    exit 1
fi

if [[ ! -w "$DIRETORIO_SAIDA" ]]; then
    printf 'Erro: diretório de saída sem permissão de escrita: %s\n' "$DIRETORIO_SAIDA" >&2
    exit 1
fi

ARQUIVO_TEMPORARIO="${SAIDA}.tmp.$$"
trap 'rm -f -- "$ARQUIVO_TEMPORARIO"' EXIT HUP INT TERM

if ! gerar_relatorio > "$ARQUIVO_TEMPORARIO"; then
    printf 'Erro: falha ao gerar o relatório: %s\n' "$SAIDA" >&2
    exit 1
fi

if ! mv -- "$ARQUIVO_TEMPORARIO" "$SAIDA"; then
    printf 'Erro: falha ao gravar o relatório: %s\n' "$SAIDA" >&2
    exit 1
fi

trap - EXIT HUP INT TERM
printf 'Relatório criado: %s\n' "$SAIDA"
