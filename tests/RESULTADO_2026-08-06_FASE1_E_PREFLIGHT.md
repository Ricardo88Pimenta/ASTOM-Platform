# Resultado de testes — Detecção ampliada e pré-flight de recuperação

**Data:** 06/08/2026  
**Versão:** `0.1.0-dev`  
**Ambiente:** contêiner isolado, Linux x86_64, Python 3.13.5 e Bash 5.2.37  
**Classificação:** homologação H1 controlada

## Artefatos testados

- `core/astom-planejar.py`;
- `core/astom-preflight-recuperacao.py`;
- `profiles/cachyos-kde-wayland-base.json`;
- `tests/teste-planejamento.sh`;
- `tests/teste-perfil-referencia.sh`;
- `tests/teste-preflight-recuperacao.sh`.

## Resultado consolidado

| Suíte | Aprovados | Reprovados |
|---|---:|---:|
| Planejamento e detecção | 14 | 0 |
| Perfil de referência | 4 | 0 |
| Pré-flight de recuperação | 10 | 0 |
| **Total desta rodada** | **28** | **0** |

## Capacidades validadas

- detecção de comandos;
- consulta de pacotes Pacman em ambiente simulado;
- consulta de Flatpaks em ambiente simulado;
- tratamento de detector indisponível;
- comparação exata de versão;
- saída JSON estruturada;
- rejeição de schema, tipo e campos inválidos;
- gravação atômica;
- privacidade básica;
- ausência de chamadas mutáveis conhecidas;
- avaliação segura de ambiente fora do alvo;
- gate de recuperação apto e bloqueado;
- tratamento de configuração Snapper raiz ausente;
- tratamento de saída Snapper malformada.

## Execução adicional no ambiente real do contêiner

O planejador processou o perfil CachyOS fora do alvo sem falhar. O pré-flight classificou o contêiner como `bloqueado para criação de snapshot`, comportamento esperado em ambiente sem Btrfs/Snapper configurados.

## Limitações

Esta rodada não homologa:

- CachyOS real;
- KDE Plasma 6 e Wayland reais;
- Btrfs e Snapper da workstation;
- criação de snapshot;
- backup de configurações;
- restauração ou rollback.

## Decisão

A detecção ampliada e o pré-flight estão aprovados em H1. A Fase 2 mutável permanece bloqueada até a homologação H2 na workstation de referência.
