# Blueprint da ASTOM Platform

**Versão:** 0.1  
**Status:** Em consolidação  
**Idioma canônico:** Português do Brasil

## 1. Propósito

Este documento organiza a visão da ASTOM Platform em partes verificáveis e implementáveis. Ele não declara módulos como prontos apenas porque foram especificados.

A ASTOM será uma camada de engenharia para workstations Linux capaz de diagnosticar o ambiente, produzir um plano de implantação, aplicar mudanças controladas, validar o resultado e executar rollback quando necessário.

## 2. Fluxo operacional pretendido

```text
Diagnóstico
    ↓
Detecção de capacidades
    ↓
Seleção de perfil
    ↓
Plano de alterações
    ↓
Confirmação explícita
    ↓
Backup e snapshot
    ↓
Implantação idempotente
    ↓
Validação
    ↓
Relatório ou rollback
```

## 3. Camadas da plataforma

### 3.1 ASTOM Core

Responsável por:

- inventário do sistema;
- detecção de distribuição, sessão gráfica e capacidades;
- leitura de manifestos;
- resolução de dependências;
- geração de planos;
- logs estruturados;
- estado da implantação.

### 3.2 ASTOM Deployment

Responsável por:

- backups;
- snapshots quando suportados;
- aplicação idempotente;
- instalação e remoção de componentes;
- validação pós-implantação;
- rollback por etapa.

### 3.3 ASTOM Profiles

Perfis declarativos para diferentes cenários:

- base profissional;
- engenharia;
- desenvolvimento;
- criação de conteúdo;
- produtividade;
- jogos;
- administração de sistemas.

### 3.4 ASTOM UI

Responsável pela experiência visual e interação:

- tokens de design;
- tema Plasma e Kvantum;
- tipografia;
- painel superior;
- dock inferior;
- launcher;
- estados, alertas e acessibilidade.

### 3.5 ASTOM Compliance

Responsável por validar componentes antes da adoção:

- licença;
- manutenção ativa;
- integridade da origem;
- permissões;
- vulnerabilidades conhecidas;
- impacto em desempenho;
- compatibilidade com Wayland;
- remoção e rollback.

## 4. Plataforma de referência inicial

A primeira referência é CachyOS com KDE Plasma 6 e Wayland. Essa escolha serve para criar e validar a primeira implementação; não transforma o CachyOS em dependência permanente da arquitetura.

## 5. Artefatos mínimos da versão 0.1 Foundation

- diagnóstico somente leitura;
- manifesto inicial da plataforma de referência;
- catálogo de componentes;
- plano de implantação sem execução;
- logs legíveis e estruturados;
- backup de configurações selecionadas;
- integração inicial com Snapper quando disponível;
- validação automatizada;
- instruções de rollback;
- relatório de teste em instalação limpa.

## 6. Regras de implementação

1. Nenhuma alteração silenciosa.
2. Nenhuma operação destrutiva sem confirmação explícita.
3. O modo de simulação deve existir antes do modo de aplicação.
4. Toda etapa mutável precisa de validação e rollback documentados.
5. Scripts devem ser idempotentes sempre que tecnicamente possível.
6. Dependências devem ser mínimas e declaradas.
7. Saídas devem distinguir sucesso, aviso e falha.
8. O projeto não deve coletar nem transmitir telemetria por padrão.
9. Dados sensíveis não devem aparecer em relatórios.
10. Compatibilidade só será declarada após teste reproduzível.

## 7. Sequência de construção

### Marco A — Diagnóstico seguro

- inventário somente leitura;
- relatório local;
- nenhuma exigência de `sudo`;
- testes de sintaxe e execução.

### Marco B — Planejamento

- manifestos declarativos;
- comparação entre estado atual e desejado;
- plano sem alterações.

### Marco C — Implantação controlada

- backup;
- snapshot;
- aplicação por componente;
- validação;
- rollback.

### Marco D — Experiência visual

- tokens;
- tema;
- painel;
- dock;
- launcher;
- acessibilidade.

### Marco E — Reprodutibilidade

- instalação limpa;
- máquina virtual;
- segunda distribuição;
- CI;
- versão candidata.

## 8. Definição de pronto

Um recurso só será marcado como concluído quando houver:

- código ou configuração versionados;
- documentação de uso;
- teste executado;
- resultado registrado;
- risco conhecido documentado;
- procedimento de remoção ou rollback.
