# Política de homologação da ASTOM Platform

A ASTOM diferencia validação controlada, homologação na plataforma-alvo e liberação de funções mutáveis.

## Níveis

### H0 — Revisão estática

- sintaxe válida;
- manifesto válido;
- ausência de chamadas mutáveis conhecidas;
- documentação mínima.

### H1 — Ambiente controlado

- execução em ambiente isolado;
- testes automatizados aprovados;
- falhas tratadas sem sucesso falso;
- saídas estruturadas e privacidade básica;
- nenhuma alteração fora dos arquivos de relatório solicitados.

### H2 — Workstation de referência

- CachyOS;
- KDE Plasma 6;
- Wayland;
- Btrfs;
- Snapper;
- hardware e serviços reais da workstation;
- resultados revisados antes da publicação.

### H3 — Instalação limpa

- máquina virtual ou equipamento de teste;
- instalação reproduzível;
- teste de backup, snapshot, validação e rollback;
- documentação completa de falhas e recuperação.

### H4 — Candidato a lançamento

- CI estável;
- matriz de compatibilidade;
- auditoria de segurança;
- licença e governança definidas;
- release assinada.

## Gate atual

- diagnóstico: **H1 aprovado**;
- planejador: **H1 aprovado**;
- perfil CachyOS/KDE/Wayland: **H1 aprovado fora do alvo**;
- pré-flight de recuperação: **H1 aprovado**;
- homologação H2: **pendente**.

Enquanto H2 estiver pendente, a ASTOM não liberará instalação de pacotes, alteração de configurações, criação de snapshots ou rollback automatizado.
