#!/usr/bin/env bash

set -uo pipefail
RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PREFLIGHT="$RAIZ/core/astom-preflight-recuperacao.py"
TEMP="$(mktemp -d -t astom-preflight.XXXXXXXX)"
trap 'rm -rf -- "$TEMP"' EXIT HUP INT TERM
APROVADOS=0
REPROVADOS=0
ok(){ printf 'APROVADO: %s\n' "$1"; APROVADOS=$((APROVADOS+1)); }
falha(){ printf 'REPROVADO: %s — %s\n' "$1" "$2" >&2; REPROVADOS=$((REPROVADOS+1)); }

if python3 -m py_compile "$PREFLIGHT"; then ok 'sintaxe Python'; else falha 'sintaxe Python' 'compilação falhou'; fi

mkdir -p "$TEMP/apto" "$TEMP/bloqueado"
cat > "$TEMP/apto/findmnt" <<'FAKE'
#!/usr/bin/env bash
if [[ "$*" == *'FSTYPE'* ]]; then printf 'btrfs\n'; else printf '/dev/mapper/astom-root\n'; fi
FAKE
cat > "$TEMP/apto/btrfs" <<'FAKE'
#!/usr/bin/env bash
printf 'btrfs-progs v6.15\n'
FAKE
cat > "$TEMP/apto/snapper" <<'FAKE'
#!/usr/bin/env bash
if [[ "$*" == *'list-configs'* ]]; then
  printf 'root,/\nuser-home,/home\n'
  exit 0
fi
exit 1
FAKE
chmod +x "$TEMP/apto/findmnt" "$TEMP/apto/btrfs" "$TEMP/apto/snapper"

if PATH="$TEMP/apto:/usr/bin:/bin" python3 "$PREFLIGHT" --output "$TEMP/apto.md" --json-output "$TEMP/apto.json" >"$TEMP/apto.out" 2>"$TEMP/apto.err" \
  && [[ -s "$TEMP/apto.md" && -s "$TEMP/apto.json" ]] \
  && grep -Fq 'apto para teste controlado de snapshot' "$TEMP/apto.md" \
  && grep -Fq '| root | / |' "$TEMP/apto.md" \
  && [[ ! -s "$TEMP/apto.err" ]]; then ok 'ambiente apto'; else falha 'ambiente apto' 'gate ou saída incorretos'; fi

cat > "$TEMP/bloqueado/findmnt" <<'FAKE'
#!/usr/bin/env bash
if [[ "$*" == *'FSTYPE'* ]]; then printf 'ext4\n'; else printf '/dev/vda1\n'; fi
FAKE
chmod +x "$TEMP/bloqueado/findmnt"
if PATH="$TEMP/bloqueado:/usr/bin:/bin" python3 "$PREFLIGHT" --output "$TEMP/bloqueado.md" >"$TEMP/bloqueado.out" 2>"$TEMP/bloqueado.err" \
  && grep -Fq 'bloqueado para criação de snapshot' "$TEMP/bloqueado.md" \
  && grep -Fq '| ext4 | bloqueado | sim |' "$TEMP/bloqueado.md"; then ok 'ambiente bloqueado degrada com segurança'; else falha 'ambiente bloqueado degrada com segurança' 'gate incorreto'; fi

mkdir -p "$TEMP/sem-raiz"
cp "$TEMP/apto/findmnt" "$TEMP/sem-raiz/findmnt"
cp "$TEMP/apto/btrfs" "$TEMP/sem-raiz/btrfs"
cat > "$TEMP/sem-raiz/snapper" <<'FAKE'
#!/usr/bin/env bash
printf 'home,/home\n'
FAKE
chmod +x "$TEMP/sem-raiz"/*
if PATH="$TEMP/sem-raiz:/usr/bin:/bin" python3 "$PREFLIGHT" --output "$TEMP/sem-raiz.md" \
  && grep -Fq 'Configuração Snapper associada à raiz | não encontrada | bloqueado' "$TEMP/sem-raiz.md"; then ok 'configuração raiz ausente'; else falha 'configuração raiz ausente' 'não bloqueou o gate'; fi

mkdir -p "$TEMP/malformado"
cp "$TEMP/apto/findmnt" "$TEMP/malformado/findmnt"
cp "$TEMP/apto/btrfs" "$TEMP/malformado/btrfs"
cat > "$TEMP/malformado/snapper" <<'FAKE'
#!/usr/bin/env bash
printf 'linha-sem-segunda-coluna\n'
FAKE
chmod +x "$TEMP/malformado"/*
if PATH="$TEMP/malformado:/usr/bin:/bin" python3 "$PREFLIGHT" --output "$TEMP/malformado.md" \
  && grep -Fq 'saída não reconhecida' "$TEMP/malformado.md" \
  && grep -Fq 'bloqueado para criação de snapshot' "$TEMP/malformado.md"; then ok 'saída Snapper malformada'; else falha 'saída Snapper malformada' 'não bloqueou com segurança'; fi

if python3 - "$TEMP/apto.json" <<'PY'
import json, sys
p=json.load(open(sys.argv[1], encoding='utf-8'))
assert p['mode'] == 'read-only'
assert p['gate'] == 'apto para teste controlado de snapshot'
assert any(c['config']=='root' and c['subvolume']=='/' for c in p['snapper_configs'])
assert all('hostname' not in c for c in p['checks'])
PY
then ok 'saída JSON estruturada'; else falha 'saída JSON estruturada' 'conteúdo inconsistente'; fi

set +e
python3 "$PREFLIGHT" --output "$TEMP/inexistente/relatorio.md" >"$TEMP/inexistente.out" 2>"$TEMP/inexistente.err"
RC=$?
set -e
if [[ $RC -ne 0 ]] && grep -Fq 'diretório de saída inexistente' "$TEMP/inexistente.err" && ! grep -Fq 'Pré-flight criado' "$TEMP/inexistente.out"; then ok 'diretório de saída inexistente'; else falha 'diretório de saída inexistente' "retorno $RC"; fi

HOST="$(hostname 2>/dev/null || true)"
IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
PRIVADO=0
for DADO in "$HOST" "$IP"; do [[ -n "$DADO" ]] && grep -Fq "$DADO" "$TEMP/apto.md" && PRIVADO=1; done
if [[ $PRIVADO -eq 0 ]]; then ok 'privacidade básica'; else falha 'privacidade básica' 'identificador encontrado'; fi

if python3 - "$PREFLIGHT" <<'PYSTATIC'
import ast, re, sys
arvore=ast.parse(open(sys.argv[1], encoding='utf-8').read())
mutaveis=re.compile(r'(^|\s)(sudo|snapper (create|delete|rollback)|btrfs subvolume (create|delete)|cp|rsync|tar)($|\s)')
for no in ast.walk(arvore):
    if not isinstance(no, ast.Call): continue
    nome=''
    if isinstance(no.func, ast.Attribute) and isinstance(no.func.value, ast.Name): nome=f'{no.func.value.id}.{no.func.attr}'
    if nome=='os.system': raise SystemExit(1)
    if nome in {'subprocess.run','subprocess.Popen'}:
        for kw in no.keywords:
            if kw.arg=='shell' and isinstance(kw.value, ast.Constant) and kw.value.value is True: raise SystemExit(1)
        if no.args and isinstance(no.args[0], (ast.List, ast.Tuple)):
            partes=[x.value for x in no.args[0].elts if isinstance(x, ast.Constant) and isinstance(x.value,str)]
            if mutaveis.search(' '.join(partes)): raise SystemExit(1)
PYSTATIC
then ok 'ausência de operações mutáveis'; else falha 'ausência de operações mutáveis' 'chamada mutável encontrada'; fi

if ! find "$TEMP" -name '.*.tmp' -print -quit | grep -q .; then ok 'limpeza de arquivos temporários'; else falha 'limpeza de arquivos temporários' 'resíduo encontrado'; fi

printf '\nResumo: %d aprovado(s), %d reprovado(s).\n' "$APROVADOS" "$REPROVADOS"
[[ $REPROVADOS -eq 0 ]]
