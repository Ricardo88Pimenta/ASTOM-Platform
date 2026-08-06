#!/usr/bin/env bash

set -uo pipefail
RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PERFIL="$RAIZ/profiles/cachyos-kde-wayland-base.json"
PLANEJADOR="$RAIZ/core/astom-planejar.py"
TEMP="$(mktemp -d -t astom-perfil.XXXXXXXX)"
trap 'rm -rf -- "$TEMP"' EXIT HUP INT TERM
APROVADOS=0
REPROVADOS=0
ok(){ printf 'APROVADO: %s\n' "$1"; APROVADOS=$((APROVADOS+1)); }
falha(){ printf 'REPROVADO: %s — %s\n' "$1" "$2" >&2; REPROVADOS=$((REPROVADOS+1)); }

if python3 -m json.tool "$PERFIL" >/dev/null; then ok 'JSON do perfil'; else falha 'JSON do perfil' 'formato inválido'; fi

if python3 - "$PERFIL" <<'PY'
import json, sys
p=json.load(open(sys.argv[1], encoding='utf-8'))
assert p['schema_version'] == 1
assert p['id'] == 'cachyos-kde-wayland-base'
ids=[c['id'] for c in p['components']]
assert len(ids) == len(set(ids))
assert {'command','package','flatpak'} <= {c['type'] for c in p['components']}
assert all(isinstance(c['required'], bool) for c in p['components'])
assert p['target']['distribution_ids'] == ['cachyos']
assert 'wayland' in p['target']['session_types']
assert 'btrfs' in p['target']['root_filesystems']
PY
then ok 'invariantes do perfil'; else falha 'invariantes do perfil' 'estrutura inconsistente'; fi

if python3 "$PLANEJADOR" --manifest "$PERFIL" --output "$TEMP/plano.md" --json-output "$TEMP/plano.json" >"$TEMP/out" 2>"$TEMP/err" \
  && [[ -s "$TEMP/plano.md" && -s "$TEMP/plano.json" ]] \
  && grep -Fq 'Base profissional CachyOS' "$TEMP/plano.md" \
  && grep -Fq 'flatpak-bitwarden' "$TEMP/plano.md" \
  && [[ ! -s "$TEMP/err" ]]; then
  ok 'planejamento do perfil fora do alvo'
else
  falha 'planejamento do perfil fora do alvo' 'o planejador não degradou com segurança'
fi

if python3 - "$TEMP/plano.json" <<'PY'
import json, sys
p=json.load(open(sys.argv[1], encoding='utf-8'))
assert p['mode'] == 'read-only'
assert p['profile']['id'] == 'cachyos-kde-wayland-base'
assert len(p['components']) == 17
assert any(x['status'] == 'fora do alvo' for x in p['target'])
PY
then ok 'JSON do perfil gerado'; else falha 'JSON do perfil gerado' 'conteúdo inconsistente'; fi

printf '\nResumo: %d aprovado(s), %d reprovado(s).\n' "$APROVADOS" "$REPROVADOS"
[[ $REPROVADOS -eq 0 ]]
