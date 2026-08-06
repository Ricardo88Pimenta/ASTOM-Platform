# Linguagem de design da ASTOM

## 1. Direção

A ASTOM adota uma linguagem visual profissional, escura, confortável e duradoura. A referência conceitual vem de design industrial e automotivo premium: superfícies precisas, materiais sóbrios, hierarquia clara e movimento controlado.

A plataforma não deverá copiar a identidade de macOS, Windows, elementary OS ou qualquer fabricante automotivo.

## 2. Princípios visuais

- função antes do ornamento;
- legibilidade antes da transparência;
- consistência antes da variedade;
- animação como orientação, não distração;
- densidade adequada a monitores grandes;
- espaço negativo para reduzir fadiga visual;
- componentes reconhecíveis sem depender de efeitos chamativos;
- estados de segurança e homologação sempre visíveis.

## 3. Aparência-base

- modo escuro como padrão;
- grafite, antracite e cinzas quentes em vez de preto absoluto;
- contraste suficiente para leitura prolongada;
- transparência moderada;
- desfoque discreto;
- sombras leves e coerentes;
- cantos e raios consistentes;
- ausência de neon, RGB e estética cyberpunk.

## 4. Tipografia

- **Inter:** interface e textos de sistema;
- **JetBrains Mono:** terminal, código, logs e dados monoespaçados;
- **Noto:** cobertura ampla de idiomas e símbolos;
- **Liberation:** compatibilidade métrica com documentos;
- **Cascadia Code e IBM Plex:** opções complementares, sujeitas à especificação de uso.

A interface deve manter fallbacks locais e nunca depender de fontes baixadas durante a execução.

## 5. Estrutura da área de trabalho

### Painel superior

Elemento primário e permanente para estado do sistema, relógio, conectividade, áudio, energia, notificações e tarefas essenciais.

### Dock inferior

Elemento secundário, centralizado, para aplicativos fixados, aplicativos em execução e troca rápida de contexto. A dock não deverá reproduzir a aparência do macOS.

### Launcher

Direção aprovada:

- centralizado;
- organização em grade;
- categorias compreensíveis;
- busca rápida;
- hierarquia clara;
- inspiração na simplicidade organizacional do elementary OS, sem cópia visual.

## 6. Movimento e acessibilidade

- transições suaves e curtas;
- aceleração e desaceleração naturais;
- nenhuma animação deve bloquear interação;
- efeitos devem poder ser reduzidos ou desativados;
- movimento deve explicar mudança de estado ou localização;
- foco de teclado sempre visível;
- navegação principal com landmarks semânticos;
- cores de estado não podem ser o único meio de comunicação;
- interface responsiva e utilizável com escalas diferentes.

## 7. Ícones e marca

- nenhuma iconografia da Apple;
- nenhuma reprodução de marcas de terceiros;
- ícones devem manter coerência de espessura, proporção e linguagem;
- logotipo e identidade ASTOM terão política própria de uso;
- o símbolo experimental do P1 não constitui marca definitiva.

## 8. Tokens experimentais P1

O protótipo P1 introduziu tokens versionados em `ui/control-center/tokens.json`.

### Direção cromática

- fundo principal: `#0e1114`;
- superfícies: `#191e23`, `#20262c` e `#262d34`;
- texto principal: `#edf0f1`;
- texto secundário: `#9fa8ae`;
- acento cobre discreto: `#d58353`;
- sucesso: `#67b98b`;
- alerta: `#d7ad62`;
- perigo: `#d97878`;
- informação: `#73a8c7`.

Esses valores são experimentais e deverão ser confirmados ou alterados após o teste real.

### Geometria e ritmo

- raios entre 8 e 22 px;
- escala de espaçamento entre 4 e 48 px;
- painel superior de referência com 58 px no Control Center;
- sidebar de referência com 220 px;
- conteúdo principal limitado a 1280 px;
- duas densidades: confortável e compacta.

### Movimento

- respostas rápidas entre 140 e 180 ms;
- transição de vista em 220 ms;
- suporte a `prefers-reduced-motion`;
- preferência manual de redução de movimento.

## 9. Protótipo funcional P1

O ASTOM Control Center implementa, para avaliação:

- navegação lateral;
- painel superior;
- cards de estado e gates;
- inventário pesquisável;
- área de recuperação;
- simulação do workspace;
- launcher em grade;
- dock inferior;
- densidades alternativas;
- checklist e feedback local.

O P1 é uma interface web local para validar linguagem visual e arquitetura da informação. Ele não é a implementação final do shell e não substitui a futura camada Qt/QML, Plasma ou Kvantum.

## 10. Critérios para evolução ao P2

- feedback real da workstation registrado;
- legibilidade aprovada em 100%, 125% e 150%;
- navegação por teclado aprovada;
- launcher e dock compreendidos sem treinamento;
- estados de segurança e homologação claramente entendidos;
- problemas de contraste e densidade corrigidos;
- decisão documentada sobre continuidade web ou migração para Qt/QML.
