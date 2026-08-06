# Pré-flight de recuperação

O pré-flight de recuperação é a primeira entrega da Fase 2, ainda em modo somente leitura.

## Objetivo

Determinar se um ambiente possui as capacidades mínimas para um futuro teste controlado de snapshot, sem criar snapshots ou backups.

## Verificações

- sistema de arquivos da raiz;
- origem do ponto de montagem raiz;
- disponibilidade da ferramenta `btrfs`;
- disponibilidade do Snapper;
- consulta das configurações Snapper;
- existência de configuração associada ao subvolume `/`.

## Gate

O resultado será um dos seguintes:

- `apto para teste controlado de snapshot`;
- `bloqueado para criação de snapshot`.

O estado apto não autoriza automaticamente a criação de snapshots. Ele apenas permite que a próxima etapa seja planejada e testada em ambiente apropriado.

## Garantias

O pré-flight:

- não utiliza `sudo`;
- não cria ou exclui snapshots;
- não executa rollback;
- não modifica Btrfs ou Snapper;
- não copia arquivos;
- grava apenas os relatórios solicitados.

## Execução

```bash
python3 core/astom-preflight-recuperacao.py \
  --output astom-preflight.md \
  --json-output astom-preflight.json
```
