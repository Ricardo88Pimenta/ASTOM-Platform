# Planejamento somente leitura

**Versão:** 0.1  
**Status:** Protótipo validado em ambiente controlado

## Objetivo

O modo de planejamento é a segunda etapa funcional da ASTOM Platform. Ele compara um perfil declarativo com capacidades detectáveis do ambiente e gera um plano em Markdown, sem instalar pacotes, modificar configurações ou controlar serviços.

## Artefatos

- planejador: `core/astom-planejar.py`;
- perfil inicial: `profiles/cachyos-kde-wayland-base.json`;
- testes: `tests/teste-planejamento.sh`;
- validação contínua: `.github/workflows/validacao.yml`.

## Fluxo

```text
Manifesto JSON
      ↓
Validação de schema
      ↓
Detecção somente leitura
      ↓
Comparação com o perfil
      ↓
Plano Markdown
```

## Execução

```bash
python3 core/astom-planejar.py \
  --manifest profiles/cachyos-kde-wayland-base.json \
  --output astom-plano.md
```

## O que o planejador detecta nesta versão

- identificador da distribuição por `/etc/os-release`;
- desktop por `XDG_CURRENT_DESKTOP`;
- tipo de sessão por `XDG_SESSION_TYPE`;
- sistema de arquivos da raiz por `findmnt`;
- presença de comandos declarados no perfil por meio do `PATH`.

## O que o planejador não faz

- não executa ações propostas;
- não instala ou remove pacotes;
- não usa `sudo`;
- não inicia, interrompe ou habilita serviços;
- não edita configurações;
- não cria snapshots;
- não decide automaticamente qual pacote deve ser instalado;
- não considera a ausência no `PATH` como prova absoluta de que um aplicativo gráfico não esteja instalado.

## Manifesto inicial

O perfil `cachyos-kde-wayland-base` declara como alvo inicial:

- CachyOS;
- KDE Plasma;
- Wayland;
- Btrfs.

Os componentes estão separados em obrigatórios e opcionais. A presença de uma ação proposta no manifesto não autoriza sua execução.

## Tratamento de erros

O planejador retorna código diferente de zero e não anuncia sucesso quando encontra:

- manifesto inexistente;
- JSON inválido;
- versão de schema incompatível;
- campos obrigatórios ausentes;
- componentes duplicados;
- tipo de componente não suportado;
- diretório de saída inexistente;
- falha de gravação.

A saída é gravada primeiro em arquivo temporário e movida atomicamente para o destino. Resíduos temporários são removidos em caso de falha.

## Critério de evolução

Antes de qualquer modo de aplicação, o planejamento deverá evoluir para:

- detecção de pacotes por gerenciador;
- identificação confiável de Flatpaks;
- comparação de versões;
- classificação de risco por ação;
- dependências entre componentes;
- geração de plano de backup;
- indicação explícita do rollback de cada etapa;
- confirmação humana obrigatória.
