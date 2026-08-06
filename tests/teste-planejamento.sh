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

mkdir -p "$TEMP/bin"
cat > "$TEMP/bin/pacman" <<'FAKE'
#!/usr/bin/env bash
if [[ ${1:-} == '-Q' && ${2:-} == 'pacote-presente' ]]; then
  printf 'pacote-presente 1.2.3-1\n'
  exit 0
fi
exit 1
FAKE
cat > "$TEMP/bin/flatpak" <<'FAKE'
#!/usr/bin/env bash
if [[ ${1:-} == 'info' && ${2:-} == '--show-version' && ${3:-} == 'com.astom.Presente' ]]; then
  printf '2.0.1\n'
  exit 0
fi
exit 1
FAKE
chmod +x "$TEMP/bin/pacman" "$TEMP/bin/flatpak"

cat > "$TEMP/manifesto.json" <<'JSON'
{
  "schema_version": 1,
  "id": "teste-controlado",
  "title": "Perfil de teste controlado",
  "target": {},
  "components": [
    {"id":"sh","type":"command","command":"sh","description":"Comando existente","required":true},
    {"id":"ausente","type":"command","command":"astom-comando-que-nao-existe-2026","description":"Comando ausente","required":true,"when_missing":"ação controlada de teste"},
    {"id":"pacote-presente","type":"package","manager":"pacman","package":"pacote-presente","description":"Pacote presente","required":true,"version":"1.2.3-1"},
    {"id":"pacote-ausente","type":"package","manager":"pacman","package":"pacote-ausente","description":"Pacote ausente","required":false},
    {"id":"flatpak-presente","type":"flatpak","app_id":"com.astom.Presente","description":"Flatpak presente","required":false,"version":"2.0.1"},
    {"id":"flatpak-ausente","type":"flatpak","app_id":"com.astom.Ausente","description":"Flatpak ausente","required":false},
    {"id":"detector-indisponivel","type":"package","manager":"zypper","package":"qualquer","description":"Detector indisponível","required":true}
  ]
}
JSON

PATH_TESTE="$TEMP/bin:/usr/bin:/bin"
if PATH="$PATH_TESTE" python3 "$PLANEJADOR" --manifest "$TEMP/manifesto.json" --output "$TEMP/plano.md" --json-output "$TEMP/plano.json" >"$TEMP/normal.out" 2>"$TEMP/normal.err" \
  && [[ -s "$TEMP/plano.md" && -s "$TEMP/plano.json" ]] \
  && grep -Fq '**Modo:** somente leitura' "$TEMP/plano.md" \
  && grep -Fq 'sh — Comando existente' "$TEMP/plano.md" \
  && grep -Fq '| presente | não aplicável | PATH | nenhuma |' "$TEMP/plano.md" \
  && [[ ! -s "$TEMP/normal.err" ]]; then ok 'geração do plano controlado'; else falha 'geração do plano controlado' 'conteúdo ou retorno inválido'; fi

if grep -Fq 'pacote-presente — Pacote presente' "$TEMP/plano.md" \
  && grep -Fq '| presente | 1.2.3-1 | pacman | nenhuma |' "$TEMP/plano.md" \
  && grep -Fq 'pacote-ausente — Pacote ausente' "$TEMP/plano.md" \
  && grep -Fq '| opcional ausente | não instalada | pacman | nenhuma |' "$TEMP/plano.md"; then ok 'detecção de pacotes pacman'; else falha 'detecção de pacotes pacman' 'estado ou versão incorretos'; fi

if grep -Fq 'flatpak-presente — Flatpak presente' "$TEMP/plano.md" \
  && grep -Fq '| presente | 2.0.1 | flatpak | nenhuma |' "$TEMP/plano.md" \
  && grep -Fq 'flatpak-ausente — Flatpak ausente' "$TEMP/plano.md"; then ok 'detecção de aplicações Flatpak'; else falha 'detecção de aplicações Flatpak' 'estado ou versão incorretos'; fi

if grep -Fq 'detector-indisponivel — Detector indisponível' "$TEMP/plano.md" \
  && grep -Fq '| detector indisponível | não identificada | zypper/rpm |' "$TEMP/plano.md"; then ok 'detector de pacotes indisponível'; else falha 'detector de pacotes indisponível' 'estado incorreto'; fi

if python3 - "$TEMP/plano.json" <<'PYJSON'
import json, sys
p = json.load(open(sys.argv[1], encoding='utf-8'))
assert p['mode'] == 'read-only'
assert p['profile']['id'] == 'teste-controlado'
assert len(p['components']) == 7
assert p['summary']['presentes'] == 3
assert p['summary']['ausentes_obrigatorios'] == 1
assert p['summary']['opcionais_ausentes'] == 2
assert p['summary']['detectores_indisponiveis'] == 1
PYJSON
then ok 'saída JSON estruturada'; else falha 'saída JSON estruturada' 'JSON inválido ou resumo incorreto'; fi

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

cat > "$TEMP/tipo.json" <<'JSON'
{"schema_version":1,"id":"x","title":"x","components":[{"id":"x","type":"servico","description":"x","required":true}]}
JSON
set +e
python3 "$PLANEJADOR" --manifest "$TEMP/tipo.json" --output "$TEMP/tipo.md" >"$TEMP/tipo.out" 2>"$TEMP/tipo.err"
RC=$?
set -e
if [[ $RC -ne 0 ]] && grep -Fq 'tipo de componente não suportado' "$TEMP/tipo.err"; then ok 'tipo de componente não suportado'; else falha 'tipo de componente não suportado' "retorno $RC"; fi

cat > "$TEMP/campo.json" <<'JSON'
{"schema_version":1,"id":"x","title":"x","components":[{"id":"x","type":"package","manager":"pacman","description":"x","required":true}]}
JSON
set +e
python3 "$PLANEJADOR" --manifest "$TEMP/campo.json" --output "$TEMP/campo.md" >"$TEMP/campo.out" 2>"$TEMP/campo.err"
RC=$?
set -e
if [[ $RC -ne 0 ]] && grep -Fq 'package precisa ser texto não vazio' "$TEMP/campo.err"; then ok 'campo obrigatório por tipo'; else falha 'campo obrigatório por tipo' "retorno $RC"; fi

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

if python3 - "$PLANEJADOR" <<'PYSTATIC'
import ast, re, sys
arvore = ast.parse(open(sys.argv[1], encoding='utf-8').read())
mutaveis = re.compile(r'(^|\s)(sudo|pacman -S|apt-get install|apt install|dnf install|zypper install|flatpak install|systemctl (start|stop|enable|disable)|snapper (create|delete|rollback))($|\s)')
for no in ast.walk(arvore):
    if not isinstance(no, ast.Call): continue
    nome = ''
    if isinstance(no.func, ast.Attribute) and isinstance(no.func.value, ast.Name): nome = f'{no.func.value.id}.{no.func.attr}'
    if nome == 'os.system': raise SystemExit(1)
    if nome in {'subprocess.run', 'subprocess.Popen'}:
        for kw in no.keywords:
            if kw.arg == 'shell' and isinstance(kw.value, ast.Constant) and kw.value.value is True: raise SystemExit(1)
        if no.args and isinstance(no.args[0], (ast.List, ast.Tuple)):
            partes = [item.value for item in no.args[0].elts if isinstance(item, ast.Constant) and isinstance(item.value, str)]
            if mutaveis.search(' '.join(partes)): raise SystemExit(1)
PYSTATIC
then ok 'ausência de execução mutável conhecida'; else falha 'ausência de execução mutável conhecida' 'chamada mutável encontrada'; fi

if ! find "$TEMP" -name '.*.tmp' -print -quit | grep -q .; then ok 'limpeza de arquivos temporários'; else falha 'limpeza de arquivos temporários' 'resíduo encontrado'; fi

printf '\nResumo: %d aprovado(s), %d reprovado(s).\n' "$APROVADOS" "$REPROVADOS"
[[ $REPROVADOS -eq 0 ]]
