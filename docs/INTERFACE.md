# ASTOM Interface — maturidade para teste real P1

## Objetivo

Disponibilizar uma primeira interface executável para avaliar linguagem visual, arquitetura da informação e leitura dos dados reais produzidos pelo ASTOM Core, sem instalar componentes nem alterar o sistema.

## Classificação

- **Protótipo:** P1 funcional;
- **homologação técnica:** H1 em ambiente controlado;
- **teste visual real:** pronto para execução local;
- **integração Plasma/Kvantum:** não iniciada;
- **operações mutáveis:** bloqueadas.

## Arquitetura

```text
Navegador local
    ↓ HTTP em 127.0.0.1
ui/astom-ui.py
    ├── arquivos estáticos locais
    ├── /api/health
    └── /api/state
          ├── astom-planejar.py
          └── astom-preflight-recuperacao.py
```

O servidor combina as saídas JSON dos dois coletores e as entrega à interface. Os coletores permanecem somente leitura.

## Escopo funcional

- visão geral da homologação e do perfil;
- resumo de componentes;
- compatibilidade da plataforma-alvo;
- tabela pesquisável e filtrável;
- gate e verificações de recuperação;
- protótipo interativo do workspace;
- launcher em grade;
- dock inferior centralizada;
- painel superior;
- densidade confortável e compacta;
- preferência de redução de movimento;
- checklist e exportação local de feedback.

## Segurança

- bind local em `127.0.0.1` por padrão;
- exposição remota exige `--allow-remote` explícito;
- métodos POST, PUT, PATCH e DELETE bloqueados;
- Content Security Policy restritiva;
- sem bibliotecas, fontes ou serviços externos;
- sem telemetria;
- sem persistência de dados do sistema no servidor;
- arquivos temporários dos coletores são removidos ao fim de cada consulta.

## Teste real

### Demonstração visual

```bash
python3 ui/astom-ui.py \
  --fixture ui/control-center/demo-state.json \
  --open
```

### Dados reais da workstation

```bash
python3 ui/astom-ui.py --open
```

A segunda opção executa apenas o planejador e o pré-flight já homologados em H1. Ela não instala, remove, configura ou cria snapshots.

## Critério de aprovação P1

O protótipo P1 será aprovado após:

- abrir corretamente na workstation de referência;
- apresentar os dados reais sem erro;
- manter legibilidade em 100%, 125% e 150% de escala;
- funcionar com teclado;
- launcher e filtros responderem sem falhas;
- feedback local ser exportado;
- nenhuma alteração de sistema ocorrer durante a sessão.

## Limites conhecidos

Este protótipo valida experiência e informação. Ele não prova ainda:

- integração nativa com KDE Plasma;
- desempenho de um shell QML;
- tema Kvantum;
- comportamento multimonitor do desktop final;
- acessibilidade com leitores de tela específicos;
- instalação reproduzível da ASTOM UI.
