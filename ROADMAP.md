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
- validação contínua inicial com GitHub Actions.

### Em andamento

- histórico formal de decisões;
- política de licenciamento;
- catálogo de componentes;
- critérios objetivos de certificação;
- consolidação da estrutura de diretórios;
- refinamento do Blueprint.

## Fase 1 — ASTOM Core mínimo

### Concluído

- diagnóstico somente leitura em Bash;
- tratamento seguro e atômico da saída do diagnóstico;
- suíte de regressão do diagnóstico com 10 testes aprovados;
- manifesto declarativo inicial do perfil CachyOS/KDE/Wayland;
- validação de schema do manifesto;
- planejador somente leitura em Python;
- comparação inicial entre alvo e ambiente;
- geração de plano Markdown sem alterações;
- suíte do planejador com 8 grupos de teste aprovados.

### Em andamento

- inventário mais completo de hardware e software;
- detecção de distribuição e capacidades;
- detecção de pacotes por gerenciador;
- detecção de aplicações Flatpak;
- comparação de versões;
- logging estruturado;
- testes na workstation de referência;
- testes em instalação limpa.

### Planejado

- composição de múltiplos perfis;
- dependências entre componentes;
- classificação de risco por ação;
- exportação de relatório estruturado para consumo por outras interfaces.

## Fase 2 — Deployment e rollback

### Planejado

- backup de configurações;
- integração inicial com snapshots Btrfs/Snapper;
- aplicação idempotente;
- validação pós-instalação;
- rollback por componente;
- relatório final de alterações.

> Nenhuma ação mutável será liberada antes de backup, validação e rollback testados.

## Fase 3 — Perfil de referência CachyOS/KDE

### Em andamento

- manifesto base para CachyOS, KDE Plasma 6, Wayland e Btrfs.

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

### Planejado

- tokens de design;
- paleta;
- tipografia e espaçamento;
- tema Plasma/Kvantum;
- launcher;
- painel superior;
- dock inferior;
- acessibilidade;
- redução de movimento.

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

O próximo marco é ampliar o inventário e a detecção do ASTOM Core para identificar pacotes e Flatpaks de forma confiável, mantendo todo o fluxo em modo somente leitura.

Depois disso, serão especificados e testados o plano de backup e a integração com Snapper. Somente após esses mecanismos será considerada qualquer função de aplicação.

## Critério para a versão 1.0

A versão 1.0 não será definida por aparência ou quantidade de recursos. Ela exigirá instalação reproduzível, validação documentada, rollback testado, compatibilidade declarada e ausência de discrepâncias conhecidas entre documentação e implementação.
