# Roadmap da ASTOM Platform

## Convenções

- **Concluído:** existe artefato verificável e testado.
- **Em andamento:** existe trabalho iniciado, mas ainda incompleto.
- **Planejado:** definido conceitualmente, sem implementação concluída.

## Fase 0 — Fundação

### Concluído

- criação do repositório oficial;
- definição do idioma canônico em português do Brasil;
- definição da missão, visão e princípios;
- registro do estado real da workstation de referência;
- documentação inicial de arquitetura, segurança e linguagem visual;
- separação entre máquina configurada e produto ASTOM implementado;
- Blueprint inicial;
- plano de testes;
- validação contínua inicial com GitHub Actions;
- política formal de níveis de homologação H0 a H4.

### Em andamento

- histórico formal de decisões;
- política de licenciamento;
- catálogo de componentes;
- critérios objetivos de certificação;
- consolidação da estrutura de diretórios;
- refinamento do Blueprint.

## Fase 1 — ASTOM Core mínimo

### Concluído em H1 controlado

- diagnóstico somente leitura em Bash;
- tratamento seguro e atômico da saída do diagnóstico;
- suíte de regressão do diagnóstico com 10 testes aprovados;
- manifesto declarativo inicial do perfil CachyOS/KDE/Wayland;
- validação de schema do manifesto;
- planejador somente leitura em Python;
- comparação inicial entre alvo e ambiente;
- geração de plano Markdown sem alterações;
- detecção de comandos pelo `PATH`;
- detecção de pacotes por Pacman, APT, DNF e Zypper;
- detecção de aplicações Flatpak;
- comparação exata de versões;
- exportação JSON estruturada;
- suíte ampliada do planejador com 14 testes aprovados;
- validação do perfil de referência com 4 testes aprovados.

### Em andamento

- inventário mais completo de hardware;
- comparação semântica de versões;
- logging estruturado persistente;
- testes na workstation de referência;
- testes em instalação limpa.

### Planejado

- composição de múltiplos perfis;
- dependências entre componentes;
- classificação de risco por ação;
- exportação para outras interfaces.

## Gate de homologação da Fase 1

- H0 — revisão estática: concluída;
- H1 — ambiente controlado: concluída;
- H2 — workstation CachyOS/KDE/Wayland: pendente;
- H3 — instalação limpa: pendente.

A Fase 1 ainda não está homologada para implantação real enquanto H2 permanecer pendente.

## Fase 2 — Deployment e rollback

### Em andamento, somente leitura

- pré-flight de recuperação;
- detecção de Btrfs;
- detecção das ferramentas Btrfs e Snapper;
- consulta de configurações Snapper;
- verificação de configuração associada à raiz;
- gate de prontidão para futuro teste controlado de snapshot;
- suíte do pré-flight com 10 testes aprovados.

### Planejado e bloqueado

- backup de configurações;
- criação controlada de snapshot;
- aplicação idempotente;
- validação pós-instalação;
- rollback por componente;
- relatório final de alterações.

> Nenhuma ação mutável será liberada antes da homologação H2, de backup verificável e de rollback testado.

## Fase 3 — Perfil de referência CachyOS/KDE

### Em andamento

- manifesto base para CachyOS, KDE Plasma 6, Wayland e Btrfs;
- capacidades, pacotes Pacman e Flatpaks declarados.

### Planejado

- perfil reproduzível para Plasma 6 e Wayland;
- tipografia;
- aplicações-base;
- segurança mínima;
- desempenho;
- áudio;
- jogos como módulo opcional;
- documentação de instalação limpa.

## Fase 4 — ASTOM UI

### Concluído em P1/H1 controlado

- tokens experimentais de cor, espaçamento, raios, tipografia e movimento;
- Control Center local e responsivo;
- integração com as saídas JSON do planejador e do pré-flight;
- visão geral, compatibilidade, componentes e recuperação;
- filtros de componentes;
- protótipo interativo de painel superior, launcher e dock;
- densidade confortável e compacta;
- redução de movimento;
- navegação por teclado e landmarks semânticos;
- exportação local de feedback;
- servidor restrito a loopback por padrão;
- Content Security Policy e bloqueio de métodos mutáveis;
- suíte de interface com 14 testes aprovados.

### Pronto para teste real

- avaliação visual P1 na workstation de referência;
- leitura de dados reais do ASTOM Core;
- teste em escalas de 100%, 125% e 150%;
- teste de teclado, launcher, filtros e exportação de feedback.

### Planejado após P1

- refinamento dos tokens com base no feedback;
- protótipo nativo Qt/QML;
- integração Plasma/Kvantum;
- comportamento multimonitor;
- testes ampliados de acessibilidade;
- empacotamento reproduzível da interface.

## Fase 5 — Perfis profissionais

### Planejado

- engenharia;
- desenvolvimento;
- criação de conteúdo;
- produtividade;
- jogos;
- administração de sistemas.

## Fase 6 — Suporte multidistribuição

### Planejado

- segunda distribuição de referência;
- abstração de gerenciadores de pacotes;
- matriz de compatibilidade;
- testes em máquina virtual;
- documentação de limitações.

## Fase 7 — Pré-lançamento

### Planejado

- licença definitiva;
- governança;
- política de marca;
- contribuição externa;
- SBOM;
- assinatura de lançamentos;
- ampliação do pipeline de CI;
- auditoria de segurança;
- versão candidata.

## Próximo marco verificável

Executar na workstation de referência uma sessão H2/P1 usando o Control Center somente leitura. A sessão deverá validar os dados reais, a legibilidade, a interação e a ausência de alterações no sistema. Depois da análise do feedback, será decidido se o próximo protótipo visual será P2 web ou a primeira implementação Qt/QML.

## Critério para a versão 1.0

A versão 1.0 exigirá instalação reproduzível, validação documentada, rollback testado, compatibilidade declarada e ausência de discrepâncias conhecidas entre documentação e implementação.
