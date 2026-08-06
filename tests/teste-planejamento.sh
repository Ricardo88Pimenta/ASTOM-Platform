#!/usr/bin/env bash

set -uo pipefail

RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PLANEJADOR="$RAIZ/core/astom-planejar.py"
TEMP="$(mktemp -d -t astom-planejamento.XXXXXXXX)"
APROVADOS=0
REPROVADOS=0
trap 'rm -rf -- "$TEMP"' EXIT HUP INT TERM

ok(){ printf 'APROVADO: %s\n' "$1"; APROVADOS=$((APROVADOS+1)); }
falha(){ printf 'REPROVADO: %s — %s\n' "$1" "$2" >&2; REPROVADOS=$((REPROVADOS+1)); }

if python3 -m py_compile "$PLANEJADOR"; then ok 'sintaxe Python'; else falha 'sintaxe Python' 'compilação falhou'; fi

cat > "$TEMP/manifesto.json" <<'JSON'
{
  "schema_version": 1,
  "id": "teste-controlado",
  "title": "Perfil de teste controlado",
  "target": {},
  "components": [
    {
      "id": "sh",
      "type": "command",
      "command": "sh",
      "description": "Comando existente",
      "required": true
    },
    {
      "id": "ausente",
      "type": "command",
      "command": "astom-comando-que-nao-existe-2026",
      "description": "Comando ausente",
      "required": true,
      "when_missing": "ação controlada de teste"
    }
  ]
}
JSON

if python3 "$PLANEJADOR" --manifest "$TEMP/manifesto.json" --output "$TEMP/plano.md" >"$TEMP/normal.out" 2>"$TEMP/normal.err" \
  && [[ -s "$TEMP/plano.md" ]] \
  && grep -Fq '**Modo:** somente leitura' "$TEMP/plano.md" \
  && grep -Fq 'sh — Comando existente' "$TEMP/plano.md" \
  && grep -Fq '| presente | nenhuma |' "$TEMP/plano.md" \
  && grep -Fq 'ausente — Comando ausente' "$TEMP/plano.md" \
  && grep -Fq 'ação controlada de teste' "$TEMP/plano.md" \
  && [[ ! -s "$TEMP/normal.err" ]]; then
  ok 'geração do plano controlado'
else
  falha 'geração do plano controlado' 'conteúdo ou retorno inválido'
fi

printf '{ inválido' > "$TEMP/invalido.json"
set +e
python3 "$PLANEJADOR" --manifest "$TEMP/invalido.json" --output "$TEMP/invalido.md" >"$TEMP/invalido.out" 2>"$TEMP/invalido.err"
RC=$?
set -e
if [[ $RC -ne 0 ]] && grep -Fq 'manifesto JSON inválido' "$TEMP/invalido.err" && [[ ! -e "$TEMP/invalido.md" ]]; then ok 'manifesto JSON inválido'; else falha 'manifesto JSON inválido' "retorno $RC"; fi

cat > "$TEMP/schema.json" <<'JSON'
{"schema_version": 99, "id": "x", "title": "x", "components": []}
JSON
set +e
python3 "$PLANEJADOR" --manifest "$TEMP/schema.json" --output "$TEMP/schema.md" >"$TEMP/schema.out" 2>"$TEMP/schema.err"
RC=$?
set -e
if [[ $RC -ne 0 ]] && grep -Fq 'schema_version incompatível' "$TEMP/schema.err" && [[ ! -e "$TEMP/schema.md" ]]; then ok 'schema incompatível'; else falha 'schema incompatível' "retorno $RC"; fi

set +e
python3 "$PLANEJADOR" --manifest "$TEMP/manifesto.json" --output "$TEMP/nao-existe/plano.md" >"$TEMP/saida.out" 2>"$TEMP/saida.err"
RC=$?
set -e
if [[ $RC -ne 0 ]] && grep -Fq 'diretório de saída inexistente' "$TEMP/saida.err" && ! grep -Fq 'Plano criado' "$TEMP/saida.out"; then ok 'diretório de saída inexistente'; else falha 'diretório de saída inexistente' "retorno $RC"; fi

HOST="$(hostname 2>/dev/null || true)"
USER_NAME="$(id -un 2>/dev/null || true)"
IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
PRIVADO=0
for DADO in "$HOST" "$USER_NAME" "$IP"; do [[ -n "$DADO" ]] && grep -Fq "$DADO" "$TEMP/plano.md" && PRIVADO=1; done
if [[ $PRIVADO -eq 0 ]]; then ok 'privacidade básica'; else falha 'privacidade básica' 'identificador encontrado'; fi

if ! grep -Eq 'subprocess\.(run|Popen).*shell[[:space:]]*=[[:space:]]*True|os\.system|sudo|apt(-get)?[[:space:]]+install|pacman[[:space:]]+-S|dnf[[:space:]]+install' "$PLANEJADOR"; then ok 'ausência de execução mutável conhecida'; else falha 'ausência de execução mutável conhecida' 'padrão encontrado'; fi

if ! find "$TEMP" -name '.*.tmp' -print -quit | grep -q .; then ok 'limpeza de arquivos temporários'; else falha 'limpeza de arquivos temporários' 'resíduo encontrado'; fi

printf '\nResumo: %d aprovado(s), %d reprovado(s).\n' "$APROVADOS" "$REPROVADOS"
[[ $REPROVADOS -eq 0 ]]
