# ASTOM Platform

> **Elegância através da Engenharia.**

A **ASTOM Platform** é uma plataforma aberta para workstations Linux, independente de distribuição, criada para oferecer uma experiência profissional baseada em engenharia, segurança, desempenho, produtividade e design atemporal.

A ASTOM não nasce como uma distribuição Linux, um tema para KDE Plasma ou uma coleção de scripts. O projeto define uma arquitetura completa de experiência para workstations: linguagem visual, implantação, segurança, perfis de uso, integração com aplicativos, atualização, validação e rollback.

## Estado do projeto

- **Fase atual:** fundação e documentação técnica
- **Versão de trabalho:** `0.1.0-dev`
- **Idioma canônico:** português do Brasil
- **Primeira plataforma de referência:** CachyOS com KDE Plasma 6 e Wayland
- **Objetivo arquitetural:** independência de distribuição e adaptação por capacidades do sistema

> O repositório documenta separadamente o que já está funcional, o que está especificado e o que ainda é apenas planejado. Percentuais informais usados durante a concepção não representam implementação concluída.

## O que já está funcional na workstation de referência

- CachyOS com KDE Plasma 6 em Wayland;
- Btrfs com Snapper e snapshots pré/pós-transação;
- systemd-boot com imagens UKI;
- Limine mantido como rota de recuperação;
- Plymouth no fluxo de inicialização;
- driver NVIDIA, Vulkan e OpenGL validados;
- PipeWire e WirePlumber ativos;
- TRIM semanal e zRAM ativos;
- UFW ativo;
- ambiente gamer com Steam, Heroic, Lutris, Proton, Wine, MangoHud, GameMode, Gamescope e GOverlay;
- GitHub Desktop, Bitwarden e Tor Browser Launcher via Flatpak;
- fontes Inter, JetBrains Mono, Cascadia Code, IBM Plex, Liberation e Noto instaladas;
- Kvantum para Qt 6 e Qt 5 instalado como motor visual experimental.

Esses itens representam a **máquina de referência** e não, ainda, uma instalação automatizada da ASTOM Platform.

## Visão

Transformar computadores Linux em ferramentas de trabalho confiáveis, elegantes e duradouras, permitindo que profissionais concentrem seu tempo em criar, projetar, desenvolver e inovar.

## Missão

Projetar uma experiência coerente e reproduzível para workstations Linux profissionais, sem aprisionamento a uma distribuição específica.

## Princípios fundamentais

1. Segurança antes da estética.
2. Confiabilidade antes de novidade.
3. Rollback antes de alteração destrutiva.
4. Engenharia antes de efeitos visuais.
5. Independência de distribuição por detecção de capacidades.
6. Design escuro, confortável e atemporal.
7. Componentes mantidos, auditáveis e removíveis.
8. Documentação em português brasileiro como fonte canônica.

## O que a ASTOM não é

- Não é uma distribuição Linux;
- não é um clone do macOS;
- não é um tema pronto para Plasma;
- não é um pacote de personalização visual;
- não é um instalador que executa alterações irreversíveis;
- não promete compatibilidade universal antes de testes reais.

## Arquitetura proposta

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

A arquitetura está em especificação. Os módulos ainda não devem ser considerados implementados apenas por estarem listados.

## Direção de design

A identidade visual será inspirada em design industrial e automotivo premium, sem copiar marcas ou sistemas operacionais existentes.

Características definidas:

- modo escuro como padrão;
- grafite e antracite em vez de preto absoluto;
- transparência e desfoque moderados;
- animações suaves e discretas;
- painel superior permanente para status e tarefas;
- dock inferior centralizada e secundária;
- launcher centralizado, em grade, inspirado na clareza do elementary OS;
- nenhuma iconografia ou logotipo da Apple;
- sem neon, RGB ou estética cyberpunk;
- tipografia Inter para interface e JetBrains Mono para código e terminal;
- muito espaço negativo, adequado a monitores grandes.

## Segurança e manutenção

Cada componente candidato deverá registrar finalidade, licença, dependências, permissões, atividade de manutenção, riscos, impacto em desempenho, compatibilidade, instalação, validação e rollback.

## Licenciamento

A licença pública definitiva ainda não foi escolhida. Até uma decisão formal, o repositório não concede automaticamente direitos de reutilização além do permitido pela legislação aplicável.

A direção em avaliação é:

- código: MPL 2.0 ou GPLv3;
- documentação: CC BY-SA 4.0;
- nome, identidade e logotipo ASTOM: política própria de marca.

Consulte `POLITICA_DE_LICENCIAMENTO.md`.

## Documentação

- [`docs/ESTADO_ATUAL.md`](docs/ESTADO_ATUAL.md)
- [`docs/VISAO_E_PRINCIPIOS.md`](docs/VISAO_E_PRINCIPIOS.md)
- [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md)
- [`docs/SEGURANCA.md`](docs/SEGURANCA.md)
- [`docs/DESIGN_LANGUAGE.md`](docs/DESIGN_LANGUAGE.md)
- [`docs/HISTORICO_DE_DECISOES.md`](docs/HISTORICO_DE_DECISOES.md)
- [`ROADMAP.md`](ROADMAP.md)
- [`CHANGELOG.md`](CHANGELOG.md)

---

**ASTOM Platform — Elegância através da Engenharia.**