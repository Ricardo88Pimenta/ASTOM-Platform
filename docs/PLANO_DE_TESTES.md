# Plano de testes da ASTOM Platform

**Versão:** 0.1  
**Status:** Ativo para o protótipo de diagnóstico

## 1. Objetivo

Estabelecer testes verificáveis antes que a ASTOM execute qualquer alteração na workstation. O primeiro artefato testável é o diagnóstico somente leitura em `core/astom-diagnostico.sh`.

## 2. Regra de segurança

O diagnóstico inicial:

- não deve exigir `sudo`;
- não deve instalar ou remover pacotes;
- não deve alterar arquivos de configuração;
- não deve iniciar, parar ou habilitar serviços;
- não deve criar snapshots;
- deve escrever apenas o relatório no caminho informado pelo usuário.

## 3. Teste 0 — Revisão do código

Antes da execução:

```bash
less core/astom-diagnostico.sh
```

Confirmar que o script contém apenas comandos de consulta e a gravação do relatório.

## 4. Teste 1 — Sintaxe

```bash
bash -n core/astom-diagnostico.sh
```

**Resultado esperado:** nenhuma saída e código de retorno `0`.

Para conferir o retorno:

```bash
bash -n core/astom-diagnostico.sh
echo $?
```

## 5. Teste 2 — Execução sem privilégios

```bash
bash core/astom-diagnostico.sh
```

**Resultado esperado:** criação de um arquivo semelhante a:

```text
astom-diagnostico-2026-08-06_11-30-00.md
```

O terminal deve informar o nome do relatório criado.

## 6. Teste 3 — Caminho de saída explícito

```bash
bash core/astom-diagnostico.sh "$HOME/astom-relatorio.md"
```

**Resultado esperado:** relatório criado exatamente no caminho informado.

## 7. Teste 4 — Conteúdo mínimo

O relatório deve conter:

- distribuição;
- kernel;
- arquitetura;
- desktop e tipo de sessão;
- sistema de arquivos da raiz;
- detecção do Snapper;
- bootloader quando identificável;
- GPU e driver NVIDIA quando disponíveis;
- PipeWire e WirePlumber;
- zRAM;
- UFW;
- componentes encontrados no `PATH`.

## 8. Teste 5 — Privacidade

Revisar o relatório e confirmar que ele não contém:

- endereço IP;
- nome de usuário;
- hostname;
- número de série;
- credenciais;
- caminhos de documentos pessoais;
- conteúdo de arquivos do usuário.

## 9. Teste 6 — Efeito colateral

Antes e depois da execução, conferir:

```bash
git status --short
systemctl --failed
```

A única mudança esperada fora do repositório é o arquivo de relatório solicitado. Nenhum serviço deve falhar em decorrência do diagnóstico.

## 10. Ambientes de teste

### Prioridade 1

- CachyOS;
- KDE Plasma 6;
- Wayland;
- Btrfs;
- Snapper;
- GPU NVIDIA.

### Prioridade 2

- máquina virtual CachyOS limpa;
- CachyOS sem Snapper;
- sessão X11;
- GPU AMD ou Intel.

### Prioridade 3

- segunda distribuição baseada em Arch;
- distribuição não baseada em Arch.

## 11. Registro de resultado

Cada teste deverá registrar:

```text
Data:
Commit testado:
Distribuição:
Desktop:
Sessão:
Hardware relevante:
Comando executado:
Resultado esperado:
Resultado obtido:
Avisos:
Falhas:
Decisão:
```

Não publicar relatórios contendo informações pessoais sem revisão.

## 12. Critério de aprovação do primeiro protótipo

O diagnóstico será aprovado como `0.1.0-alpha` quando:

- passar na validação de sintaxe;
- executar sem `sudo`;
- não produzir alterações no sistema;
- gerar relatório legível na workstation de referência;
- tratar comandos ausentes sem interromper a execução;
- não expor dados sensíveis;
- tiver pelo menos um resultado de teste registrado.
