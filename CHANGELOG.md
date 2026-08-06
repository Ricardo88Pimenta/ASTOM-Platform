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
- workflow de validação contínua em `.github/workflows/validacao.yml`;
- relatório atualizado do teste controlado.

### Corrigido

- falha que retornava código `0` quando o diretório de saída do diagnóstico não existia;
- mensagem falsa de sucesso após falha de gravação;
- ausência de validação do diretório de destino;
- risco de permanência de arquivo parcial durante a geração do relatório.

### Validado

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

### Esclarecido

- a workstation de referência está funcional e amplamente configurada;
- os módulos ASTOM Core, UI, Workspace, Deployment e Compliance ainda estão em especificação;
- percentuais informais de progresso não representam implementação comprovada;
- itens só serão tratados como concluídos quando houver artefato verificável e teste correspondente;
- o diagnóstico permanece em `0.1.0-dev` até ser validado na workstation CachyOS/KDE de referência.

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
