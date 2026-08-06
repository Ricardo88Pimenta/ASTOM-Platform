# Estado atual da ASTOM Platform

**Versão da documentação:** 0.1  
**Data de referência:** 06/08/2026  
**Status:** Fundação arquitetural e documentação inicial

## 1. Objetivo deste documento

Este documento separa com clareza:

1. o que já está funcional na workstation usada como referência;
2. o que já foi decidido em arquitetura;
3. o que ainda não foi implementado;
4. quais são os próximos marcos verificáveis.

## 2. Workstation de referência

A primeira máquina de referência utiliza:

- CachyOS;
- KDE Plasma 6;
- sessão Wayland;
- GPU NVIDIA GTX 1060 6 GB;
- driver NVIDIA proprietário validado;
- CPU Ryzen 7 9800X3D;
- placa-mãe Gigabyte B650M Gaming Plus WiFi.

## 3. Itens já funcionais

### 3.1 Inicialização e recuperação

- systemd-boot ativo;
- imagens UKI em uso;
- Plymouth integrado ao fluxo de inicialização;
- Limine mantido como rota adicional de recuperação;
- Btrfs ativo;
- Snapper configurado;
- snapshots automáticos pré e pós-transação;
- rollback disponível no nível do sistema de arquivos.

### 3.2 Gráficos e jogos

- driver NVIDIA funcional;
- Vulkan validado;
- OpenGL validado;
- Steam instalada;
- Proton habilitado;
- Heroic Games Launcher instalado;
- Lutris instalado;
- Wine disponível;
- MangoHud instalado, incluindo bibliotecas de 32 bits;
- GameMode funcional;
- Gamescope e GOverlay disponíveis.

### 3.3 Áudio, armazenamento e memória

- PipeWire ativo;
- WirePlumber ativo;
- TRIM periódico configurado;
- zRAM ativa.

### 3.4 Segurança e aplicações

- UFW ativo;
- Bitwarden Desktop instalado;
- GitHub Desktop instalado;
- Tor Browser Launcher instalado via Flatpak;
- Nextcloud Desktop disponível;
- Okular e PDF Arranger disponíveis;
- Spectacle adotado como ferramenta de captura.

### 3.5 Tipografia e camada visual

- fontes do Windows importadas para compatibilidade;
- Inter instalada;
- JetBrains Mono instalada;
- Cascadia Code instalada;
- IBM Plex instalada;
- Liberation instalada;
- Noto instalada;
- Kvantum para Qt 6 e Qt 5 instalado como motor experimental.

## 4. Itens definidos, mas ainda não implementados como produto ASTOM

- ASTOM Core;
- motor de detecção de capacidades;
- perfis de workstation;
- instalador reproduzível;
- mecanismo de validação pós-instalação;
- rollback automatizado por componente;
- launcher próprio;
- painel e dock padronizados;
- catálogo certificado de componentes;
- testes automatizados;
- suporte formal a múltiplas distribuições;
- sistema de atualização da própria plataforma.

## 5. Interpretação correta do progresso

A workstation de referência está amplamente preparada e validada para uso diário. Isso não significa que a ASTOM Platform esteja 50%, 60% ou qualquer outro percentual implementada.

O estado real do projeto de software é:

- concepção: avançada;
- documentação: iniciada;
- arquitetura: em consolidação;
- implementação do produto: ainda inicial;
- testes automatizados: não iniciados;
- distribuição pública: não iniciada.

## 6. Critério de conclusão da versão 0.1 Foundation

A versão 0.1 Foundation só será considerada concluída quando existirem:

- documentação arquitetural mínima;
- catálogo inicial de componentes;
- especificação do ASTOM Core;
- instalador em modo simulação;
- rotina de backup;
- rotina de rollback;
- validação em uma instalação limpa;
- registro dos testes executados.
