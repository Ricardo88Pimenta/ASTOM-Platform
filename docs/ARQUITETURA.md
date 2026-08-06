# Arquitetura inicial

## 1. Princípio central

A ASTOM Platform será independente de distribuição por meio de **detecção de capacidades**, não por listas rígidas de distribuições suportadas.

O sistema deverá identificar recursos disponíveis, gerenciadores de pacotes, sessão gráfica, sistema de arquivos, bootloader, serviços e permissões antes de propor qualquer alteração.

## 2. Camadas

```text
ASTOM Platform
├── ASTOM Core
├── ASTOM UI
├── ASTOM Workspace
├── ASTOM Security
├── ASTOM Deployment
├── ASTOM Update e Rollback
├── ASTOM Profiles
├── ASTOM Integrations
├── ASTOM Compliance
└── ASTOM Documentation
```

### 2.1 ASTOM Core

Responsável por:

- inventário da máquina;
- detecção de capacidades;
- leitura de perfis;
- planejamento de alterações;
- execução controlada;
- validação;
- registro de estado;
- acionamento de rollback.

O Core não deverá depender de uma interface gráfica específica.

### 2.2 ASTOM UI

Responsável pela camada visual e pela aplicação da linguagem de design.

A primeira implementação de referência será voltada ao KDE Plasma 6 em Wayland, sem transformar o projeto em uma dependência exclusiva do Plasma.

### 2.3 ASTOM Workspace

Responsável por cenários de uso, organização de aplicativos, atalhos, áreas de trabalho, painéis, dock e perfis profissionais.

### 2.4 ASTOM Security

Responsável por políticas de privilégio mínimo, isolamento, auditoria, integridade, atualização segura e redução de superfície de ataque.

### 2.5 ASTOM Deployment

Responsável por transformar uma especificação declarativa em um plano de implantação verificável.

Fluxo esperado:

```text
Inventário → Compatibilidade → Plano → Backup → Simulação → Aplicação → Validação → Registro
```

### 2.6 ASTOM Update e Rollback

Toda alteração relevante deverá possuir:

- estado anterior conhecido;
- backup ou snapshot;
- validação pós-alteração;
- procedimento de reversão;
- log compreensível.

### 2.7 ASTOM Profiles

Perfis não serão apenas listas de pacotes. Cada perfil representará um cenário de trabalho, por exemplo:

- engenharia;
- desenvolvimento;
- criação de conteúdo;
- produtividade geral;
- jogos;
- administração de sistemas.

### 2.8 ASTOM Integrations

Camada destinada a aplicativos e serviços externos, sem exigir que sejam absorvidos pelo núcleo da plataforma.

### 2.9 ASTOM Compliance

Responsável por verificar se componentes e configurações atendem aos critérios técnicos, de segurança, licença, manutenção e desempenho.

## 3. Regras arquiteturais

- nenhuma alteração destrutiva sem confirmação e rollback;
- nenhuma dependência visual deve controlar o Core;
- nenhuma distribuição deve ser tratada como padrão universal;
- componentes opcionais devem permanecer removíveis;
- configurações devem ser declarativas sempre que possível;
- detecção deve preceder instalação;
- idempotência será requisito para rotinas de implantação;
- falhas parciais devem ser detectadas e reportadas;
- logs não devem expor segredos.

## 4. Estado desta arquitetura

Esta arquitetura é uma especificação inicial aprovada conceitualmente. Ainda não existe implementação completa dos módulos descritos.
