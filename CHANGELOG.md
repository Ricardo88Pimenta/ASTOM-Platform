# Histórico de alterações

Todas as mudanças relevantes da ASTOM Platform serão registradas neste documento.

## [0.1.0-dev] — 06/08/2026

### Adicionado

- repositório oficial da ASTOM Platform;
- README institucional em português do Brasil;
- definição de missão, visão e princípios;
- documentação do estado atual da workstation de referência;
- arquitetura inicial em camadas;
- modelo inicial de segurança;
- linguagem de design inicial;
- roadmap de desenvolvimento;
- política provisória de licenciamento;
- primeiro diagnóstico somente leitura em `core/astom-diagnostico.sh`;
- suíte automatizada de regressão em `tests/teste-diagnostico.sh`;
- primeiro planejador somente leitura em `core/astom-planejar.py`;
- perfil declarativo `profiles/cachyos-kde-wayland-base.json`;
- suíte automatizada do planejador em `tests/teste-planejamento.sh`;
- workflow de validação contínua em `.github/workflows/validacao.yml`;
- documentação do modo de planejamento;
- relatórios atualizados dos testes controlados.

### Corrigido

- falha que retornava código `0` quando o diretório de saída do diagnóstico não existia;
- mensagem falsa de sucesso após falha de gravação;
- ausência de validação do diretório de destino;
- risco de permanência de arquivo parcial durante a geração do relatório.

### Validado

#### Diagnóstico

- 10 testes automatizados aprovados em ambiente controlado;
- sintaxe Bash;
- execução sem privilégios administrativos;
- caminho contendo espaços;
- tratamento de diretório inexistente;
- tratamento de diretório sem escrita;
- conteúdo mínimo;
- privacidade básica;
- limpeza de arquivos temporários;
- ausência de comandos destrutivos conhecidos;
- execução com `PATH` reduzido.

#### Planejamento

- 8 grupos de testes automatizados aprovados em ambiente controlado;
- compilação e sintaxe Python;
- leitura e validação de manifesto JSON;
- detecção de comandos presentes e ausentes;
- rejeição de JSON inválido;
- rejeição de schema incompatível;
- tratamento de falha na saída;
- privacidade básica;
- gravação atômica e limpeza de temporários;
- ausência de ações mutáveis conhecidas.

### Esclarecido

- a workstation de referência está funcional e amplamente configurada;
- os módulos ASTOM UI, Workspace, Deployment e Compliance ainda estão em especificação;
- o ASTOM Core possui apenas os primeiros protótipos somente leitura;
- percentuais informais de progresso não representam implementação comprovada;
- itens só serão tratados como concluídos quando houver artefato verificável e teste correspondente;
- diagnóstico e planejador permanecem em `0.1.0-dev` até validação na workstation CachyOS/KDE de referência;
- nenhuma função de implantação foi liberada.

### Plataforma de referência registrada

- CachyOS;
- KDE Plasma 6;
- Wayland;
- Btrfs e Snapper;
- systemd-boot com UKI;
- Limine como recuperação adicional;
- NVIDIA, Vulkan e OpenGL validados;
- PipeWire, WirePlumber, TRIM e zRAM;
- UFW;
- stack de jogos e aplicações-base;
- fontes profissionais e Kvantum instalados.
