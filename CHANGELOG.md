# Histórico de alterações

Todas as mudanças relevantes da ASTOM Platform serão registradas neste documento.

## [0.1.0-dev] — 06/08/2026

### Adicionado

- repositório oficial e documentação institucional;
- arquitetura, segurança, linguagem visual, Blueprint e roadmap;
- diagnóstico somente leitura em `core/astom-diagnostico.sh`;
- planejador somente leitura em `core/astom-planejar.py`;
- suporte a componentes `command`, `package` e `flatpak`;
- consulta de pacotes Pacman, APT, DNF e Zypper;
- comparação exata de versões;
- saída JSON estruturada do planejador;
- perfil ampliado `profiles/cachyos-kde-wayland-base.json`;
- pré-flight de recuperação em `core/astom-preflight-recuperacao.py`;
- consulta somente leitura de Btrfs e configurações Snapper;
- política de homologação H0 a H4;
- documentação da detecção de componentes e do pré-flight;
- testes automatizados e workflow de validação contínua.

### Corrigido

- tratamento de falhas de gravação do diagnóstico;
- mensagem falsa de sucesso após falha;
- risco de arquivo parcial durante geração de relatórios;
- validações de campos específicos por tipo de componente.

### Validado

#### Diagnóstico

- 10 testes aprovados em ambiente controlado.

#### Planejamento e detecção

- 14 testes aprovados;
- comandos, pacotes e Flatpaks;
- saída Markdown e JSON;
- erros de schema e manifesto;
- detectores indisponíveis;
- privacidade básica;
- ausência de ações mutáveis conhecidas.

#### Perfil de referência

- 4 testes aprovados;
- JSON, invariantes, tipos de componente e degradação segura fora do alvo.

#### Pré-flight de recuperação

- 10 testes aprovados;
- gates apto e bloqueado;
- configuração Snapper raiz ausente;
- saída Snapper malformada;
- JSON estruturado;
- gravação atômica e ausência de operações mutáveis.

### Estado de homologação

- H1 controlado: aprovado para diagnóstico, planejamento, perfil e pré-flight;
- H2 workstation de referência: pendente;
- instalação de pacotes, criação de snapshots, backup e rollback: bloqueados.

### Plataforma de referência registrada

- CachyOS;
- KDE Plasma 6;
- Wayland;
- Btrfs e Snapper;
- systemd-boot com UKI;
- NVIDIA, Vulkan e OpenGL;
- PipeWire, WirePlumber, TRIM, zRAM e UFW;
- stack de jogos e aplicações-base.
