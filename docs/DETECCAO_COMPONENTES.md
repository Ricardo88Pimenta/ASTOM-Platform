# Detecção de componentes

O planejador ASTOM suporta três tipos de componente no schema 1.

## `command`

Verifica apenas se um executável está disponível no `PATH`.

Campos:

- `id`;
- `type: command`;
- `command`;
- `description`;
- `required`.

## `package`

Consulta um pacote instalado sem executar instalação, atualização ou remoção.

Gerenciadores suportados:

- `pacman`;
- `apt`, usando `dpkg-query`;
- `dnf`, usando `rpm`;
- `zypper`, usando `rpm`.

Campos adicionais:

- `manager`;
- `package`;
- `version`, opcional.

A versão declarada é comparada por igualdade exata. Faixas semânticas ainda não são suportadas.

## `flatpak`

Consulta um aplicativo pelo identificador Flatpak.

Campos adicionais:

- `app_id`;
- `version`, opcional.

## Estados

- `presente`;
- `ausente`;
- `opcional ausente`;
- `versão divergente`;
- `detector indisponível`.

## Saídas

O planejador gera:

- relatório Markdown;
- inventário JSON opcional com `--json-output`.

Todas as consultas são executadas sem shell, sem `sudo` e com timeout. O planejador não instala, atualiza ou remove componentes.
