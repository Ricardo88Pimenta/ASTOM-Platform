# Resultado de teste — Diagnóstico ASTOM

**Data:** 06/08/2026  
**Artefato:** `core/astom-diagnostico.sh`  
**Versão declarada:** `0.1.0-dev`  
**Ambiente:** contêiner isolado baseado em Debian 13 (Trixie), arquitetura x86_64  
**Classificação:** validação preliminar fora da workstation de referência

## Objetivo

Verificar se o primeiro diagnóstico da ASTOM:

- possui sintaxe Bash válida;
- executa sem privilégios administrativos;
- trata a ausência de componentes opcionais;
- cria um relatório Markdown;
- inclui o cabeçalho e a indicação de modo somente leitura.

## Testes executados

### Sintaxe

```bash
bash -n core/astom-diagnostico.sh
```

**Resultado:** aprovado, código de retorno `0`.

### Execução

```bash
bash core/astom-diagnostico.sh /tmp/astom-relatorio.md
```

**Resultado:** aprovado, código de retorno `0`.

### Arquivo de saída

Validações:

- arquivo criado;
- arquivo não vazio;
- título `Relatório de diagnóstico ASTOM` presente;
- indicação `Modo: somente leitura` presente.

**Resultado:** aprovado.

## Resultado observado

O relatório foi criado com 71 linhas no ambiente de teste e identificou corretamente:

- Debian GNU/Linux 13 (Trixie);
- kernel e arquitetura;
- ausência de ambiente gráfico no contêiner;
- gerenciador de pacotes `apt`;
- componentes disponíveis e indisponíveis sem interromper a execução.

## Limitações deste teste

Este teste não valida ainda:

- CachyOS;
- KDE Plasma 6;
- sessão Wayland;
- systemd-boot/UKI;
- Snapper real;
- GPU NVIDIA;
- PipeWire e WirePlumber em sessão de usuário;
- UFW na workstation;
- ausência absoluta de efeitos colaterais fora do ambiente isolado.

## Decisão

O script está apto para o **primeiro teste manual na workstation de referência**, desde que seja executado sem `sudo` e o relatório seja revisado antes de qualquer publicação.

Este resultado não promove o diagnóstico para versão estável. A aprovação `0.1.0-alpha` depende do teste na workstation CachyOS/KDE de referência.
