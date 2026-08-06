#!/usr/bin/env bash

# ASTOM Platform — Testes de regressão do diagnóstico

set -uo pipefail

RAIZ_REPOSITORIO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="${RAIZ_REPOSITORIO}/core/astom-diagnostico.sh"
TEMPORARIO="$(mktemp -d -t astom-diagnostico.XXXXXXXX)"
APROVADOS=0
REPROVADOS=0
IGNORADOS=0

finalizar() {
    rm -rf -- "$TEMPORARIO"
}
trap finalizar EXIT HUP INT TERM

aprovar() {
    printf 'APROVADO: %s\n' "$1"
    APROVADOS=$((APROVADOS + 1))
}

reprovar() {
    printf 'REPROVADO: %s — %s\n' "$1" "$2" >&2
    REPROVADOS=$((REPROVADOS + 1))
}

ignorar() {
    printf 'IGNORADO: %s — %s\n' "$1" "$2"
    IGNORADOS=$((IGNORADOS + 1))
}

if [[ ! -f "$SCRIPT" ]]; then
    printf 'Erro: script não encontrado: %s\n' "$SCRIPT" >&2
    exit 1
fi

mkdir -p -- \
    "$TEMPORARIO/normal" \
    "$TEMPORARIO/com espacos" \
    "$TEMPORARIO/sem-escrita"

if bash -n "$SCRIPT"; then
    aprovar 'sintaxe Bash'
else
    reprovar 'sintaxe Bash' 'código inválido'
fi

SAIDA_NORMAL="$TEMPORARIO/normal/relatorio.md"
if SAIDA_TERMINAL="$(bash "$SCRIPT" "$SAIDA_NORMAL" 2>"$TEMPORARIO/normal/erro")" \
    && [[ -s "$SAIDA_NORMAL" ]] \
    && [[ "$SAIDA_TERMINAL" == *'Relatório criado:'* ]] \
    && [[ ! -s "$TEMPORARIO/normal/erro" ]]; then
    aprovar 'execução normal'
else
    reprovar 'execução normal' 'retorno, saída ou relatório inválido'
fi

SAIDA_ESPACOS="$TEMPORARIO/com espacos/relatorio astom.md"
if bash "$SCRIPT" "$SAIDA_ESPACOS" >"$TEMPORARIO/espacos.out" 2>"$TEMPORARIO/espacos.err" \
    && [[ -s "$SAIDA_ESPACOS" ]]; then
    aprovar 'caminho contendo espaços'
else
    reprovar 'caminho contendo espaços' 'arquivo não criado corretamente'
fi

set +e
bash "$SCRIPT" "$TEMPORARIO/inexistente/sub/relatorio.md" \
    >"$TEMPORARIO/inexistente.out" 2>"$TEMPORARIO/inexistente.err"
RETORNO_INEXISTENTE=$?
set -e

if [[ $RETORNO_INEXISTENTE -ne 0 ]] \
    && grep -q 'diretório de saída inexistente' "$TEMPORARIO/inexistente.err" \
    && ! grep -q 'Relatório criado' "$TEMPORARIO/inexistente.out" \
    && [[ ! -e "$TEMPORARIO/inexistente/sub/relatorio.md" ]]; then
    aprovar 'diretório inexistente'
else
    reprovar 'diretório inexistente' "retorno obtido: $RETORNO_INEXISTENTE"
fi

chmod 555 "$TEMPORARIO/sem-escrita"
if [[ $(id -u) -eq 0 ]] && command -v runuser >/dev/null 2>&1 && id nobody >/dev/null 2>&1; then
    chmod 755 "$TEMPORARIO"
    set +e
    runuser -u nobody -- bash "$SCRIPT" "$TEMPORARIO/sem-escrita/relatorio.md" \
        >"$TEMPORARIO/sem-escrita.out" 2>"$TEMPORARIO/sem-escrita.err"
    RETORNO_SEM_ESCRITA=$?
    set -e
elif [[ $(id -u) -ne 0 ]]; then
    set +e
    bash "$SCRIPT" "$TEMPORARIO/sem-escrita/relatorio.md" \
        >"$TEMPORARIO/sem-escrita.out" 2>"$TEMPORARIO/sem-escrita.err"
    RETORNO_SEM_ESCRITA=$?
    set -e
else
    RETORNO_SEM_ESCRITA=0
    ignorar 'diretório sem escrita' 'não foi possível executar como usuário não privilegiado'
fi

if [[ ${RETORNO_SEM_ESCRITA:-0} -ne 0 ]]; then
    if grep -q 'sem permissão de escrita' "$TEMPORARIO/sem-escrita.err" \
        && ! grep -q 'Relatório criado' "$TEMPORARIO/sem-escrita.out" \
        && [[ ! -e "$TEMPORARIO/sem-escrita/relatorio.md" ]]; then
        aprovar 'diretório sem escrita'
    else
        reprovar 'diretório sem escrita' 'tratamento de erro incorreto'
    fi
fi

SECOES_OBRIGATORIAS=(
    '# Relatório de diagnóstico ASTOM'
    '**Modo:** somente leitura'
    '## Sistema'
    '## Armazenamento, boot e recuperação'
    '## Gráficos e sessão'
    '## Áudio, memória e segurança'
    '## Componentes detectados'
    '## Observações'
)

SECAO_AUSENTE=''
for SECAO in "${SECOES_OBRIGATORIAS[@]}"; do
    if ! grep -Fq "$SECAO" "$SAIDA_NORMAL"; then
        SECAO_AUSENTE="$SECAO"
        break
    fi
done

if [[ -z "$SECAO_AUSENTE" ]]; then
    aprovar 'conteúdo mínimo'
else
    reprovar 'conteúdo mínimo' "seção ausente: $SECAO_AUSENTE"
fi

HOST_ATUAL="$(hostname 2>/dev/null || true)"
USUARIO_ATUAL="$(id -un 2>/dev/null || true)"
IP_ATUAL="$(hostname -I 2>/dev/null | awk '{print $1}')"
PRIVACIDADE_OK=1

for DADO in "$HOST_ATUAL" "$USUARIO_ATUAL" "$IP_ATUAL"; do
    if [[ -n "$DADO" ]] && grep -Fq "$DADO" "$SAIDA_NORMAL"; then
        PRIVACIDADE_OK=0
    fi
done

if [[ $PRIVACIDADE_OK -eq 1 ]]; then
    aprovar 'privacidade básica'
else
    reprovar 'privacidade básica' 'identificador do ambiente encontrado'
fi

if ! find "$TEMPORARIO" -name '*.tmp.*' -print -quit | grep -q .; then
    aprovar 'limpeza de arquivos temporários'
else
    reprovar 'limpeza de arquivos temporários' 'arquivo residual encontrado'
fi

PADRAO_DESTRUTIVO='(^|[[:space:]])(sudo|pacman[[:space:]]+-S|apt(-get)?[[:space:]]+install|dnf[[:space:]]+install|rm[[:space:]]+-rf|systemctl[[:space:]]+(start|stop|enable|disable)|snapper[[:space:]]+(create|delete|rollback))([[:space:]]|$)'
if ! grep -Eq "$PADRAO_DESTRUTIVO" "$SCRIPT"; then
    aprovar 'ausência de comandos destrutivos conhecidos'
else
    reprovar 'ausência de comandos destrutivos conhecidos' 'padrão potencialmente destrutivo encontrado'
fi

if PATH=/usr/bin:/bin bash "$SCRIPT" "$TEMPORARIO/normal/path-reduzido.md" \
    >"$TEMPORARIO/path-reduzido.out" 2>"$TEMPORARIO/path-reduzido.err" \
    && [[ -s "$TEMPORARIO/normal/path-reduzido.md" ]]; then
    aprovar 'execução com PATH reduzido'
else
    reprovar 'execução com PATH reduzido' 'diagnóstico interrompido'
fi

printf '\nResumo: %d aprovado(s), %d reprovado(s), %d ignorado(s).\n' \
    "$APROVADOS" "$REPROVADOS" "$IGNORADOS"

if [[ $REPROVADOS -ne 0 ]]; then
    exit 1
fi
