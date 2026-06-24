# Agent Rules <!-- tessl-managed -->

@.tessl/RULES.md follow the [instructions](.tessl/RULES.md)

## Diretrizes do Projeto (AI-Native & SDD - .NET 8)

Este projeto segue uma abordagem AI-Native combinada com SDD (Schema/Spec Driven Development) usando .NET 8.

---

### 🧭 Roteamento de Diretrizes (Hub de IA)

Para manter o contexto enxuto, livre de redundâncias e focado no domínio, as regras e habilidades de desenvolvimento deste repositório foram totalmente modularizadas. Consulte os links abaixo antes de realizar qualquer tarefa específica:

1. **Segurança e Operação:**
   - **Aprovação de Comandos:** As restrições de execução e segurança no terminal estão descritas em [terminal-approval-flow.md](.tessl/plugins/machinereturn/dotnet-clean-arch/rules/terminal-approval-flow.md).
   - **Gestão de Segredos:** Diretrizes para proteção de credenciais e uso de secrets locais estão em [secret-management.md](.tessl/plugins/machinereturn/dotnet-clean-arch/rules/secret-management.md).

2. **Versionamento de Código (Git):**
   - **Nomenclatura de Branches e Fluxo de Merge:** Regras para nomear branches (`<operacao>/<ticket> - <descricao>`) e para o fluxo de integração (branches integram na `develop`; `develop` integra na `main` somente com aprovação do responsável) estão em [branch-and-merge-flow.md](.tessl/plugins/machinereturn/git-versioning/rules/branch-and-merge-flow.md).
   - **Higiene do Git:** Regras para `.gitignore` e arquivos temporários de compilação estão em [git-hygiene.md](.tessl/plugins/machinereturn/git-versioning/rules/git-hygiene.md).
   - **Operação de Versionamento:** O passo a passo de criação de branch, commits e merge está na skill [git-workflow-manager](.tessl/plugins/machinereturn/git-versioning/skills/git-workflow-manager/SKILL.md).

3. **Especificações de Desenvolvimento (SDD):**

   - **Processo SDD:** A obrigatoriedade de leitura de especificações antes do início da codificação está descrita em [spec-driven-development.md](.tessl/plugins/machinereturn/sdd-workflow/rules/spec-driven-development.md).
   - **Criação e Formato de Specs:** Regras de nomenclatura e templates obrigatórios de especificação estão delegadas à skill [sdd-spec-enforcer](.tessl/plugins/machinereturn/sdd-workflow/skills/sdd-spec-enforcer/SKILL.md).

4. **Arquitetura e Implementação:**
   - **Estrutura da Solução:** A nomenclatura de projetos .csproj, .sln e dependências de arquitetura está descrita em [solution-structure.md](.tessl/plugins/machinereturn/dotnet-clean-arch/rules/solution-structure.md).
   - **Domínio Rico (DDD):** Diretrizes para Aggregate Roots, Entities e Value Objects estão na skill [rich-domain-builder](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/rich-domain-builder/SKILL.md).
   - **Fatias Verticais (Vertical Slices):** Padrões para rotas da API, Command/Query Handlers e FluentValidation estão na skill [net8-vertical-slice-generator](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/net8-vertical-slice-generator/SKILL.md).
   - **Mapeamento e Migrações (EF Core):** Regras de configuração Fluent API e geração de migrações estão na skill [efcore-config-migration-enforcer](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/efcore-config-migration-enforcer/SKILL.md).
   - **Estratégias de Cache (Redis):** Diretrizes para o padrão Cache-Aside e gerenciamento de chaves no Redis estão na skill [redis-cache-manager](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/redis-cache-manager/SKILL.md).

5. **Estratégia de Testes:**
   - **Testes Unitários:** O isolamento e a modelagem com xUnit, Moq e FluentAssertions estão na skill [xunit-moq-fluentassertions-tester](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/xunit-moq-fluentassertions-tester/SKILL.md).
   - **Testes de Integração:** O uso de Testcontainers (PostgreSQL e Redis) com xUnit e FluentAssertions está na skill [testcontainers-integration-tester](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/testcontainers-integration-tester/SKILL.md).dotnet-clean-arch/skills/testcontainers-integration-tester/SKILL.md).

Antes de codificar qualquer nova funcionalidade, localize e leia a especificação correspondente (`spec-*.md`) no diretório `/specs` ou `/docs/specs`.

---

### 🏢 Tema de Domínio: MachineReturn (Logística Reversa de Máquinas Corporativas)

Sistema de gerenciamento de devolução de máquinas corporativas por fim de contrato ou defeito, integrando triagem automática de destino e inspeção de qualidade de hardware.

#### Fluxo de Negócio e Personas

1. **Abertura de Chamado (Consumidor - Sem Login):**
   - Um consumidor abre um chamado de devolução informando apenas o **código da máquina** e o **e-mail** associado a ela.
   - O sistema valida se o e-mail corresponde ao usuário atualmente atribuído à máquina.
   - A devolução é motivada por: **Tempo de Aluguel Expirado** ou **Produto com Erro**.
2. **Triagem Automática de Fábrica:**
   - Com base no ano de fabricação, origem da máquina e número de série, o sistema calcula para qual **Fábrica Cadastrada** a máquina deve ser enviada fisicamente.
3. **Inspeção de Qualidade (Agente de Qualidade - Com Login):**
   - Na fábrica receptora, um Agente de Qualidade realiza a averiguação física.
   - Ele define o **Selo de Qualidade** da máquina: `Novo`, `UsadoEmBoasCondicoes`, `Usado`, `NecessitaManutencao`, `Desmontar`, `Descartar`.
   - Com base no selo e nas regras, o agente decide o destino operacional da máquina.

#### Entidades do Domínio (Classes Ricas)

- **Usuario e Perfil:** Perfis como `Consumidor` (sem acesso de login ao sistema) e `AgenteQualidade` (com login).
- **Maquina:** Código único, número de série, ano de fabricação, país de origem, usuário atribuído atual e histórico de selos de qualidade.
- **ChamadoDevolucao:** Ciclo de vida (`Aberto`, `EmTransito`, `Recebido`, `Inspecionado`, `Finalizado`), motivo do chamado, fábrica de destino e histórico de tramitação.
- **Fabrica:** Nome, país e capacidade operacional.
- **LaudoQualidade:** Resultado da averiguação do Agente de Qualidade contendo o selo atribuído e o parecer técnico.

#### Regra de Roteamento (Exemplo)

- **Fábrica de Destino:**
  - Máquinas com **origem** fora das Américas e **ano de fabricação** menor que 2021 são direcionadas para a Fábrica de Descarte Internacional.
  - Máquinas com **motivo** "Produto com Erro" e **número de série** iniciado com "CN" vão para a Fábrica de Manutenção Avançada.

---

### 🏛️ Arquitetura do Sistema

O projeto é estruturado utilizando conceitos de **Clean Architecture** combinados com **Vertical Slice Architecture** distribuídos nas seguintes camadas:

1. **Domain:** Contém as entidades ricas do negócio, agregados e objetos de valor.
   - *Diretriz:* Siga a skill [rich-domain-builder](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/rich-domain-builder/SKILL.md) para encapsulamento das invariantes e validações.
2. **Application:** Orquestra os casos de uso do sistema por fatias verticais (features).
   - *Diretriz:* Siga a skill [net8-vertical-slice-generator](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/net8-vertical-slice-generator/SKILL.md).
3. **Infra:** Implementa a persistência de dados (PostgreSQL via EF Core) e infraestrutura de cache (Redis).
   - *Diretriz:* Siga a skill [efcore-config-migration-enforcer](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/efcore-config-migration-enforcer/SKILL.md) para mapeamento Fluent API e criação de migrações.
   - *Diretriz:* Siga a skill [redis-cache-manager](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/redis-cache-manager/SKILL.md) para cache distribuído e estratégias de invalidação.
4. **API:** Camada de entrada (Minimal APIs/Controllers) que expõe os endpoints das fatias verticais.
5. **Shared:** Contém o middleware de tratamento global de exceções para conversão semântica de erros (ex: `DomainException` -> HTTP 400/422).

---

### 💾 Banco de Dados, Cache e Configurações Locais

- **Banco de Dados e Cache:** Utiliza PostgreSQL (persistência de escrita) e Redis (cache distribuído).
  - *Diretriz:* Consulte a skill [redis-cache-manager](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/redis-cache-manager/SKILL.md) para detalhes de gerenciamento de chaves e resiliência com Redis.
- **Orquestração Local:** A infraestrutura local é orquestrada via `docker-compose.yml` e arquivos `Dockerfile`.
- **Dados Iniciais (Seeds):** Carga automática no banco de dados para criar um usuário administrador padrão (`admin`).
- **Migrações (EF Core):** As migrações residem na camada `Infra` e devem ser aplicadas automaticamente na inicialização da API em desenvolvimento, conforme detalhado na skill [efcore-config-migration-enforcer](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/efcore-config-migration-enforcer/SKILL.md).
- **Resiliência:** Configure políticas de retry como `EnableRetryOnFailure` do EF Core para o PostgreSQL, tolerando atrasos de inicialização dos containers.
- **Segredos e Configurações:** Siga estritamente a regra de segurança descrita em [secret-management.md](.tessl/plugins/machinereturn/dotnet-clean-arch/rules/secret-management.md).

---

### 🧪 Estratégia de Testes

Toda nova funcionalidade criada deve conter testes correspondentes para garantir qualidade de ponta a ponta:

1. **Testes Unitários:** Focados na lógica do Domain e Application de forma isolada.
   - *Diretriz:* Siga a skill [xunit-moq-fluentassertions-tester](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/xunit-moq-fluentassertions-tester/SKILL.md).
2. **Testes de Integração:** Fluxos ponta a ponta em banco e cache reais e efêmeros.
   - *Diretriz:* Siga a skill [testcontainers-integration-tester](.tessl/plugins/machinereturn/dotnet-clean-arch/skills/testcontainers-integration-tester/SKILL.md).

---

### 📞 Testes Manuais (Arquivos `.http`)

- Para testes manuais rápidos na API, crie arquivos com extensão `.http` na camada de API ou no diretório `/requests` na raiz do projeto.
- **Regra:** Crie um arquivo `.http` individual para cada seção de domínio ou Aggregate Root (ex: `requests/machine-returns.http`) para manter os testes focados por contexto.
