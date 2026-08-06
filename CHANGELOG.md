# Histórico de alterações

Todas as mudanças relevantes da ASTOM Platform serão registradas neste documento.

## [0.2.0-dev] — 06/08/2026

### Adicionado — ASTOM Interface P1

- servidor local somente leitura em `ui/astom-ui.py`;
- ASTOM Control Center responsivo;
- integração com JSON do planejador e do pré-flight;
- visão geral de homologação, perfil e compatibilidade;
- inventário de componentes com busca e filtros;
- painel de recuperação e gates de segurança;
- Design Lab com painel superior, launcher e dock interativos;
- densidades confortável e compacta;
- opção de redução de movimento;
- sessão de avaliação com exportação local de feedback;
- tokens de design experimentais em JSON;
- fixture de demonstração sem dependência da plataforma-alvo;
- documentação de execução e critérios de aprovação P1;
- suíte automatizada da interface;
- validação da interface incorporada ao GitHub Actions.

### Segurança da interface

- servidor restrito a `127.0.0.1` por padrão;
- exposição remota exige autorização explícita;
- métodos mutáveis bloqueados;
- Content Security Policy restritiva;
- ausência de dependências externas e telemetria;
- arquivos temporários removidos após a coleta;
- dados do ASTOM Core apresentados somente em leitura.

### Validado — Interface P1

- 14 testes aprovados em ambiente controlado;
- sintaxe Python e JavaScript;
- semântica HTML e estrutura de acessibilidade;
- integridade básica do CSS e redução de movimento;
- contrato do estado e tokens de design;
- endpoints local de saúde e estado;
- tipos MIME e cabeçalhos de segurança;
- bloqueio de POST e outros métodos mutáveis;
- proteção contra acesso fora da pasta estática;
- integração com coletores simulados;
- rejeição de estado incompatível.

### Estado

- protótipo técnico: **P1 pronto**;
- homologação controlada: **H1 aprovada**;
- teste visual real na workstation: **pronto para execução**;
- homologação H2 e integração nativa Plasma/Qt: **pendentes**;
- backup, snapshot, instalação e rollback continuam bloqueados.

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
