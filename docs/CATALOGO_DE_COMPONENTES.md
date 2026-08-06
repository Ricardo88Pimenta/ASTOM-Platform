# Catálogo inicial de componentes

**Versão:** 0.1  
**Status:** Inventário preliminar da workstation de referência

## Convenções

- **Validado na referência:** funcionamento observado na workstation atual.
- **Candidato:** considerado para a plataforma, ainda sem certificação.
- **Experimental:** instalado ou avaliado, mas ainda sem decisão definitiva.
- **Planejado:** ainda não implementado.

A presença neste catálogo não equivale à certificação ASTOM.

## Base do sistema

| Componente | Função | Estado atual | Risco principal | Rollback inicial |
|---|---|---|---|---|
| CachyOS | Distribuição da primeira referência | Validado na referência | Acoplamento excessivo à distribuição | Manter adaptadores e manifestos separados |
| KDE Plasma 6 | Ambiente de trabalho | Validado na referência | Mudanças de API e comportamento entre versões | Preservar configurações originais |
| Wayland | Sessão gráfica | Validado na referência | Incompatibilidade de componentes antigos | Permitir fallback quando disponível |
| Btrfs | Sistema de arquivos | Validado na referência | Operações incorretas de subvolume | Diagnóstico antes de qualquer automação |
| Snapper | Snapshots e recuperação | Validado na referência | Falsa expectativa de rollback completo | Testar restauração e documentar limites |
| systemd-boot/UKI | Inicialização principal | Validado na referência | Erro de boot durante atualizações | Preservar entrada funcional e rota de recuperação |
| Limine | Rota adicional de recuperação | Validado na referência | Divergência entre carregadores | Não alterar sem plano específico |
| Plymouth | Experiência visual de boot | Validado na referência | Falha cosmética ou atraso de boot | Restaurar configuração anterior |

## Gráficos e jogos

| Componente | Função | Estado atual | Risco principal | Rollback inicial |
|---|---|---|---|---|
| Driver NVIDIA proprietário | Aceleração gráfica | Validado na referência | Incompatibilidade com kernel | Snapshot e pacote anterior disponível |
| Vulkan/OpenGL | APIs gráficas | Validado na referência | Bibliotecas 32/64 bits inconsistentes | Reinstalação declarativa de pacotes |
| Steam/Proton | Jogos | Validado na referência | Configurações específicas por jogo | Perfil opcional e removível |
| Heroic | Jogos GOG/Epic | Validado na referência | Dependências e integrações externas | Remoção sem afetar perfil base |
| Lutris/Wine | Compatibilidade e jogos | Validado na referência | Prefixos frágeis e dependências | Isolar dados e configurações |
| MangoHud | Telemetria local de desempenho | Validado na referência | Injeção incompatível em aplicativos | Desabilitar por aplicativo |
| GameMode | Ajustes temporários de desempenho | Validado na referência | Política agressiva de recursos | Desabilitar serviço e integração |
| Gamescope | Compositor para jogos | Validado na referência | Compatibilidade com drivers | Manter como módulo opcional |
| GOverlay | Configuração gráfica | Validado na referência | Alterações globais indevidas | Backup das configurações |

## Áudio, memória e armazenamento

| Componente | Função | Estado atual | Risco principal | Rollback inicial |
|---|---|---|---|---|
| PipeWire | Áudio e mídia | Validado na referência | Rotas ou perfis incorretos | Restaurar configuração do usuário |
| WirePlumber | Gerenciamento de sessão multimídia | Validado na referência | Regras personalizadas conflitantes | Remover regras ASTOM |
| zRAM | Compressão de memória | Validado na referência | Parâmetros inadequados ao hardware | Restaurar configuração anterior |
| fstrim.timer | TRIM periódico | Validado na referência | Aplicação em dispositivo inadequado | Desabilitar temporizador |

## Segurança e produtividade

| Componente | Função | Estado atual | Risco principal | Rollback inicial |
|---|---|---|---|---|
| UFW | Firewall de host | Validado na referência | Bloqueio de serviços necessários | Backup e restauração das regras |
| Bitwarden Desktop | Gerenciamento de credenciais | Validado na referência | Dependência de conta externa | Não manipular cofres ou credenciais |
| GitHub Desktop | Interface Git | Validado na referência | Configuração de credenciais | Manter fora do núcleo obrigatório |
| Tor Browser Launcher | Navegação com Tor | Validado na referência | Origem e atualização do pacote | Flatpak removível e isolado |
| Nextcloud Desktop | Sincronização de arquivos | Validado na referência | Conflitos e exposição de caminhos | Não configurar contas automaticamente |
| Okular | Leitura e anotação de documentos | Validado na referência | Baixo | Remoção simples |
| PDF Arranger | Organização de PDFs | Validado na referência | Manipulação destrutiva pelo usuário | Operar sempre em cópias |
| Spectacle | Capturas de tela | Validado na referência | Permissões de captura em Wayland | Reverter atalhos e permissões |

## Tipografia e interface

| Componente | Função | Estado atual | Risco principal | Rollback inicial |
|---|---|---|---|---|
| Inter | Tipografia de interface | Validado na referência | Métricas diferentes em aplicativos | Restaurar fonte padrão |
| JetBrains Mono | Código e terminal | Validado na referência | Baixo | Restaurar fonte anterior |
| Cascadia Code | Compatibilidade e código | Validado na referência | Baixo | Remoção simples |
| IBM Plex | Tipografia complementar | Validado na referência | Baixo | Remoção simples |
| Liberation/Noto | Compatibilidade documental | Validado na referência | Substituição de fontes não intencional | Revisar fontconfig |
| Fontes Microsoft importadas | Compatibilidade documental | Validado localmente | Licenciamento e redistribuição | Nunca redistribuir dentro do projeto |
| Kvantum Qt 5/6 | Motor visual | Experimental | Inconsistência entre aplicativos | Restaurar tema Qt/Plasma anterior |

## Componentes próprios ainda planejados

| Componente | Função | Estado |
|---|---|---|
| ASTOM Core | Diagnóstico, planejamento e estado | Protótipo inicial de diagnóstico publicado |
| ASTOM Deployment | Implantação e rollback | Planejado |
| ASTOM Profiles | Perfis declarativos | Planejado |
| ASTOM UI | Experiência visual integrada | Planejado |
| ASTOM Compliance | Certificação de componentes | Planejado |
| ASTOM Update | Atualização da plataforma | Planejado |

## Próxima revisão

O catálogo deverá evoluir para fichas individuais contendo:

- pacote e origem;
- versão mínima e máxima validada;
- licença;
- mantenedor;
- dependências;
- permissões;
- consumo de recursos;
- compatibilidade Wayland;
- testes;
- falhas conhecidas;
- instalação;
- remoção;
- rollback;
- decisão de certificação.
