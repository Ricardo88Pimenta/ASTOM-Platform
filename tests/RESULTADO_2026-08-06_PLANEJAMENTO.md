# Resultado de teste — Planejamento ASTOM

**Data:** 06/08/2026  
**Artefato:** `core/astom-planejar.py`  
**Versão declarada:** `0.1.0-dev`  
**Ambiente:** contêiner isolado baseado em Debian 13 (Trixie), arquitetura x86_64  
**Classificação:** protótipo somente leitura aprovado em ambiente controlado

## Objetivo

Validar o primeiro gerador de plano da ASTOM Platform e confirmar que ele interpreta um manifesto declarativo, detecta componentes sem alterar o sistema e trata erros de entrada e saída corretamente.

## Rastreabilidade

- commit do planejador: `d341baf32e5b5d41a36dfd97b7940b98b0d6395d`;
- blob do planejador validado: `58b7589360b7835d7e182db198c8a67a552d52bb`;
- commit do perfil inicial: `0ae70e7942e5368e96add75d8a8bc3f67ca72f23`;
- blob do perfil validado: `c9e6a6d6226a78437b71067150d843f3e434286f`;
- commit da suíte de testes: `c5ab7564ca9fca774eb7a87f291aa105b52bfca2`;
- blob da suíte validado: `b536363cbb7260caf7ad889d34e2fc8df765bea6`.

Os hashes dos artefatos testados no ambiente controlado correspondem aos blobs publicados no GitHub.

## Testes executados

| Teste | Resultado |
|---|---:|
| Compilação e sintaxe Python | Aprovado |
| Geração de plano controlado | Aprovado |
| Detecção de comando presente | Aprovado |
| Detecção de comando obrigatório ausente | Aprovado |
| Tratamento de JSON inválido | Aprovado |
| Rejeição de schema incompatível | Aprovado |
| Tratamento de diretório de saída inexistente | Aprovado |
| Privacidade básica | Aprovado |
| Ausência de execução mutável conhecida | Aprovado |
| Limpeza de arquivos temporários | Aprovado |

A suíte automatizada consolida esses controles em oito grupos de teste.

## Resultado consolidado

- **Grupos aprovados:** 8;
- **Grupos reprovados:** 0;
- **código de retorno da suíte:** `0`;
- **alterações no sistema:** nenhuma;
- **privilégios administrativos:** não utilizados.

## Validação do perfil inicial

O perfil `cachyos-kde-wayland-base.json` foi validado como JSON e processado pelo planejador.

Como o ambiente controlado utiliza Debian, sem sessão gráfica, e sistema de arquivos diferente do alvo, o plano classificou corretamente distribuição, desktop, sessão e sistema de arquivos como `fora do alvo`. Essa divergência é esperada e demonstra que o planejador não declara compatibilidade indevida.

## Limites

Esta validação ainda não comprova o comportamento em:

- CachyOS real;
- KDE Plasma 6;
- Wayland;
- Btrfs e Snapper;
- workstation com todos os componentes do perfil;
- detecção de pacotes instalados fora do `PATH`.

## Decisão

O planejador e o manifesto inicial estão aprovados como protótipos somente leitura em `0.1.0-dev`.

Nenhum modo de aplicação foi liberado. A próxima evolução deverá ampliar a detecção e definir backup e rollback antes de qualquer ação mutável.
