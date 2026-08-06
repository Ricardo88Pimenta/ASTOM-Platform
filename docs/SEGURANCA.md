# Modelo inicial de segurança

## 1. Objetivo

A segurança da ASTOM Platform deverá ser estrutural, verificável e reversível. A plataforma não poderá depender apenas de boas práticas informais ou da habilidade do operador.

## 2. Princípios

- segurança por padrão;
- privilégio mínimo;
- redução da superfície de ataque;
- alterações auditáveis;
- segredos fora de logs e repositório;
- backups antes de mudanças críticas;
- rollback obrigatório;
- validação pós-alteração;
- dependências mínimas;
- componentes com manutenção ativa;
- nenhuma elevação de privilégio permanente sem justificativa.

## 3. Ciclo seguro de alteração

```text
Detectar → Avaliar risco → Planejar → Criar ponto de retorno → Simular → Aplicar → Validar → Registrar
```

Se a validação falhar, o sistema deverá interromper o fluxo e oferecer reversão segura.

## 4. Critérios para componentes

Cada componente deverá informar:

- origem;
- licença;
- mantenedores;
- frequência de atualização;
- dependências;
- permissões;
- serviços criados;
- portas expostas;
- arquivos modificados;
- consumo estimado de recursos;
- compatibilidade com Wayland;
- procedimento de remoção;
- procedimento de rollback;
- riscos conhecidos.

## 5. Supply chain

A plataforma deverá preferir:

1. repositórios oficiais da distribuição;
2. Flatpak/Flathub quando o isolamento e a manutenção forem adequados;
3. repositórios de terceiros somente com justificativa;
4. pacotes AUR ou equivalentes somente após avaliação explícita;
5. scripts remotos nunca executados diretamente sem inspeção e fixação de versão.

## 6. Estado da máquina de referência

Na workstation inicial já estão presentes mecanismos úteis à futura implementação:

- Btrfs;
- Snapper;
- snapshots automáticos;
- UFW;
- systemd-boot com UKI;
- Limine como rota adicional de recuperação;
- Flatpak para parte das aplicações.

Esses mecanismos ainda não estão orquestrados por um ASTOM Core.

## 7. Dados e privacidade

A ASTOM deverá:

- coletar o mínimo possível;
- não enviar telemetria sem consentimento explícito;
- permitir uso totalmente local;
- explicar qualquer integração externa;
- armazenar configurações de maneira legível;
- nunca versionar chaves, tokens, senhas ou identificadores sensíveis.

## 8. Limites atuais

Não existe ainda auditoria automatizada, scanner de dependências, assinatura de lançamentos, SBOM ou pipeline de segurança. Esses itens fazem parte do roadmap e só serão marcados como concluídos após implementação e teste.
