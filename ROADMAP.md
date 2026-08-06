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
- separação entre máquina configurada e produto ASTOM implementado.

### Em andamento

- histórico formal de decisões;
- política de licenciamento;
- catálogo de componentes;
- critérios objetivos de certificação;
- definição da estrutura de diretórios;
- consolidação do Blueprint.

## Fase 1 — ASTOM Core mínimo

### Planejado

- inventário de hardware e software;
- detecção de distribuição e capacidades;
- leitura de manifesto declarativo;
- modo somente diagnóstico;
- geração de plano sem alteração;
- logging estruturado;
- testes unitários iniciais.

## Fase 2 — Deployment e rollback

### Planejado

- backup de configurações;
- integração inicial com snapshots Btrfs/Snapper;
- aplicação idempotente;
- validação pós-instalação;
- rollback por componente;
- relatório final de alterações.

## Fase 3 — Perfil de referência CachyOS/KDE

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
- pipeline de CI;
- auditoria de segurança;
- versão candidata.

## Critério para a versão 1.0

A versão 1.0 não será definida por aparência ou quantidade de recursos. Ela exigirá instalação reproduzível, validação documentada, rollback testado, compatibilidade declarada e ausência de discrepâncias conhecidas entre documentação e implementação.
