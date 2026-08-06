# ASTOM Platform

> **Elegância através da Engenharia.**

A **ASTOM Platform** é uma plataforma aberta e independente de distribuição para workstations Linux profissionais. O projeto reúne diagnóstico, perfis declarativos, planejamento, recuperação, segurança e uma experiência visual coerente, sempre com validação e rollback antes de mudanças no sistema.

A ASTOM não é uma distribuição Linux, um clone de outro sistema operacional ou uma coleção de scripts sem governança.

## Estado atual

- **Versão de trabalho:** `0.2.0-dev`
- **Idioma canônico:** português do Brasil
- **Plataforma de referência:** CachyOS, KDE Plasma 6, Wayland e Btrfs
- **Homologação controlada:** H1
- **Interface:** protótipo funcional P1 pronto para teste visual real
- **Operações mutáveis:** bloqueadas até H2, backup e rollback testados

## Entregas funcionais

### ASTOM Core — somente leitura

- diagnóstico seguro em Bash;
- planejador declarativo em Python;
- detecção de comandos, pacotes Pacman/APT/DNF/Zypper e Flatpaks;
- comparação exata de versões;
- relatórios Markdown e JSON;
- perfil de referência CachyOS/KDE/Wayland;
- pré-flight de Btrfs e Snapper;
- gates formais de homologação H0 a H4.

### ASTOM Interface P1

- Control Center local e responsivo;
- leitura dos dados reais do planejador e do pré-flight;
- visão geral, compatibilidade, inventário e recuperação;
- busca e filtros de componentes;
- protótipo de painel superior, launcher e dock;
- densidades confortável e compacta;
- redução de movimento;
- exportação local de feedback;
- servidor em `127.0.0.1` por padrão;
- nenhuma telemetria ou dependência externa.

## Testar a interface

Clone o repositório e, na raiz, execute:

```bash
python3 ui/astom-ui.py --open
```

Esse modo consulta a workstation usando apenas os coletores somente leitura.

Para avaliar apenas o design com dados simulados:

```bash
python3 ui/astom-ui.py \
  --fixture ui/control-center/demo-state.json \
  --open
```

Consulte [`docs/INTERFACE.md`](docs/INTERFACE.md) para o roteiro e os critérios do teste P1.

## Testes automatizados

Resultados controlados registrados:

- diagnóstico: **10 aprovados, 0 reprovados**;
- planejamento e detecção: **14 aprovados, 0 reprovados**;
- perfil de referência: **4 aprovados, 0 reprovados**;
- pré-flight de recuperação: **10 aprovados, 0 reprovados**;
- interface P1: **14 aprovados, 0 reprovados**.

A validação contínua verifica Bash, ShellCheck, Python, JavaScript, manifestos, coletores e interface.

## Princípios

1. Segurança antes da estética.
2. Confiabilidade antes da novidade.
3. Rollback antes de alteração destrutiva.
4. Engenharia antes de efeitos visuais.
5. Independência de distribuição por detecção de capacidades.
6. Design escuro, confortável e atemporal.
7. Componentes mantidos, auditáveis e removíveis.
8. Documentação em português brasileiro como fonte canônica.

## Arquitetura

```text
ASTOM Platform
├── Core
├── UI
├── Workspace
├── Security
├── Deployment
├── Update e Rollback
├── Profiles
├── Integrations
├── Compliance
└── Documentation
```

## Segurança do estágio atual

A interface e os coletores não instalam pacotes, não alteram configurações, não iniciam serviços e não criam snapshots. O servidor local bloqueia métodos mutáveis e aplica cabeçalhos de segurança. Backup, snapshot e rollback automatizados ainda não foram liberados.

## Documentação principal

- [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md)
- [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md)
- [`docs/SEGURANCA.md`](docs/SEGURANCA.md)
- [`docs/HOMOLOGACAO.md`](docs/HOMOLOGACAO.md)
- [`docs/DESIGN_LANGUAGE.md`](docs/DESIGN_LANGUAGE.md)
- [`docs/INTERFACE.md`](docs/INTERFACE.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`CHANGELOG.md`](CHANGELOG.md)

## Licenciamento

A licença definitiva ainda está em decisão formal. Consulte [`POLITICA_DE_LICENCIAMENTO.md`](POLITICA_DE_LICENCIAMENTO.md). Até a publicação de uma licença, não há concessão automática de direitos de reutilização além da legislação aplicável.

---

**ASTOM Platform — Elegância através da Engenharia.**
