# Linguagem de design da ASTOM

## 1. Direção

A ASTOM adotará uma linguagem visual profissional, escura, confortável e duradoura. A referência conceitual vem de design industrial e automotivo premium: superfícies precisas, materiais sóbrios, hierarquia clara e movimento controlado.

A plataforma não deverá copiar a identidade de macOS, Windows, elementary OS ou qualquer fabricante automotivo.

## 2. Princípios visuais

- função antes do ornamento;
- legibilidade antes da transparência;
- consistência antes da variedade;
- animação como orientação, não distração;
- densidade adequada a monitores grandes;
- espaço negativo para reduzir fadiga visual;
- componentes reconhecíveis sem depender de efeitos chamativos.

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

## 5. Estrutura da área de trabalho

### Painel superior

Elemento primário e permanente para:

- estado do sistema;
- relógio e calendário;
- conectividade;
- áudio;
- energia;
- notificações;
- tarefas essenciais.

### Dock inferior

Elemento secundário, centralizado, para:

- aplicativos fixados;
- aplicativos em execução;
- troca rápida de contexto.

A dock não deverá reproduzir a aparência do macOS.

### Launcher

Direção aprovada:

- centralizado;
- organização em grade;
- categorias compreensíveis;
- busca rápida;
- hierarquia clara;
- inspiração na simplicidade organizacional do elementary OS, sem cópia visual.

## 6. Movimento

- transições suaves e curtas;
- aceleração e desaceleração naturais;
- nenhuma animação deve bloquear interação;
- efeitos devem poder ser reduzidos ou desativados;
- movimento deve explicar mudança de estado ou localização.

## 7. Ícones e marca

- nenhuma iconografia da Apple;
- nenhuma reprodução de marcas de terceiros;
- ícones devem manter coerência de espessura, proporção e linguagem;
- logotipo e identidade ASTOM terão política própria de uso.

## 8. Implementação atual

Na workstation de referência, Kvantum Qt 6 e Qt 5 foi instalado para estudo da camada visual. Isso não representa um tema ASTOM concluído.

Ainda faltam:

- tokens de design;
- paleta definitiva;
- escalas tipográficas;
- sistema de espaçamento;
- especificação de componentes;
- protótipos;
- testes de acessibilidade;
- implementação reproduzível.
