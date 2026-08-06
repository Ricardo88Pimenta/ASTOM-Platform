# ASTOM Control Center — Protótipo P1

Protótipo funcional e local da interface ASTOM. Ele apresenta dados reais produzidos pelo planejador e pelo pré-flight, sem executar operações mutáveis.

## Executar com dados reais

Na raiz do repositório:

```bash
python3 ui/astom-ui.py --open
```

A aplicação é servida apenas em `127.0.0.1:8765` por padrão.

## Executar em demonstração

```bash
python3 ui/astom-ui.py \
  --fixture ui/control-center/demo-state.json \
  --open
```

## O que pode ser avaliado

- hierarquia visual e legibilidade;
- navegação e filtros;
- representação de compatibilidade e gates;
- protótipo do painel superior, launcher e dock;
- densidade confortável ou compacta;
- redução de movimento;
- exportação local de feedback.

## Limites

- não é um tema Plasma ou Kvantum;
- não substitui o shell da área de trabalho;
- não instala nem remove componentes;
- não cria backups, snapshots ou rollback;
- não envia telemetria ou feedback pela internet.
