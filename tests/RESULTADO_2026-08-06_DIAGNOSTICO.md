# Resultado de teste — Diagnóstico ASTOM

**Data:** 06/08/2026  
**Artefato:** `core/astom-diagnostico.sh`  
**Versão declarada:** `0.1.0-dev`  
**Ambiente:** contêiner isolado baseado em Debian 13 (Trixie), arquitetura x86_64  
**Classificação:** validação controlada concluída; validação na workstation de referência ainda pendente

## Objetivo

Validar a correção da falha de gravação identificada no primeiro ciclo e executar uma bateria de regressão do diagnóstico somente leitura.

## Erro corrigido

Na versão anterior, um caminho de saída cujo diretório não existia produzia erro no Bash, mas o script terminava com código `0` e mostrava incorretamente a mensagem `Relatório criado`.

A correção implementada:

- valida a existência do diretório de saída;
- valida a permissão de escrita;
- retorna código diferente de zero em caso de falha;
- não informa sucesso quando o arquivo não foi criado;
- gera o conteúdo em arquivo temporário;
- move o arquivo temporário de forma atômica para o destino;
- remove arquivos temporários em caso de interrupção ou erro.

## Rastreabilidade

- commit da correção: `e30249bd6d16734c9eff64d014f713b0028c5a7d`;
- blob validado: `aa9b15c0b2d7463087086f5b455b2e39d5a4c481`;
- teste automatizado: `tests/teste-diagnostico.sh`;
- commit do teste: `ad019f6aeac954719936222eecfa515f28ed5a83`.

O hash do blob produzido no ambiente controlado foi comparado ao hash publicado no GitHub e correspondeu exatamente.

## Testes executados

| Teste | Resultado |
|---|---:|
| Sintaxe Bash | Aprovado |
| Execução normal | Aprovado |
| Caminho contendo espaços | Aprovado |
| Diretório de saída inexistente | Aprovado |
| Diretório sem permissão de escrita | Aprovado |
| Conteúdo mínimo do relatório | Aprovado |
| Privacidade básica | Aprovado |
| Limpeza de arquivos temporários | Aprovado |
| Ausência de comandos destrutivos conhecidos | Aprovado |
| Execução com `PATH` reduzido | Aprovado |

## Resultado consolidado

- **Aprovados:** 10;
- **Reprovados:** 0;
- **Ignorados:** 0;
- **código de retorno da suíte:** `0`;
- **linhas do relatório de referência:** 71;
- **tamanho do relatório de referência:** 2.014 bytes.

## Automação adicionada

Foi criado o workflow `.github/workflows/validacao.yml` para executar, em alterações futuras:

- validação de sintaxe Bash;
- ShellCheck;
- suíte de regressão do diagnóstico.

## Limites desta validação

O ambiente controlado não reproduz:

- CachyOS;
- KDE Plasma 6;
- sessão Wayland;
- systemd-boot com UKI;
- Snapper real;
- GPU NVIDIA;
- PipeWire e WirePlumber em sessão gráfica;
- UFW da workstation de referência.

## Decisão

A correção está **aprovada no ambiente controlado** e a regressão automatizada foi incorporada ao projeto.

O diagnóstico permanece em `0.1.0-dev` até passar pelo teste somente leitura na workstation CachyOS/KDE de referência. Nenhuma função de implantação ou alteração do sistema foi liberada.
