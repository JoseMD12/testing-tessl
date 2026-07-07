# Agent Guidelines

## Diretrizes do Projeto (AI-Native & SDD - .NET 8)

Este projeto segue uma abordagem AI-Native combinada com SDD (Schema/Spec Driven Development) usando .NET 8, guiado por um Harness de Tasks de IA.

---

### 🔄 Harness de Tasks de IA (Ciclo de Vida de 3 Steps)

Toda tarefa de desenvolvimento ou modificação de código de IA neste projeto deve seguir rigorosamente o ciclo de vida de 3 passos:

1. **Research (Pesquisa):** O agente explora o codebase, localiza dependências e arquivos a serem alterados, e detalha suas descobertas nas "Research Notes" da task. *Exige aprovação do usuário rodando `./scripts/task.sh approve` para avançar.*
2. **Plan (Planejamento):** O agente projeta a arquitetura da solução e **gera o arquivo de especificação (`specs/spec-*.md`)**. O caminho do spec deve ser apontado no arquivo da task. *Exige aprovação do usuário rodando `./scripts/task.sh approve` para avançar.*
3. **Implement (Implementação):** O agente codifica a solução, escreve testes, garante que tudo funciona (build e testes passam), e roda linter. *Exige aprovação final do usuário rodando `./scripts/task.sh approve` para conclusão.*

**Como utilizar:**

- Inicializar uma task: `./scripts/task.sh init "Nome da Task"`
- Verificar status da task: `./scripts/task.sh status`
- Aprovar a fase atual: `./scripts/task.sh approve`

#### 🔄 Retomada de Contexto (Bootstrapping do Agente)

Sempre que iniciar uma nova conversa ou sessão de trabalho, o Agente de IA deve obrigatoriamente:

1. **Verificar se há uma task ativa:** Ler o conteúdo do arquivo local [tasks/.active](tasks/.active) ou rodar `./scripts/task.sh status` (ou a ferramenta MCP `harness_get_status`).
2. **Carregar o estado da task:** Ler o arquivo markdown da tarefa ativa (ex: `tasks/task-*.md`) para identificar a fase atual (`Research`, `Plan` ou `Implement`), as "Research Notes" registradas e o Spec linkado.
3. **Retomar o trabalho:** Prosseguir a partir das pendências identificadas no checklist de fases, evitando refazer análises ou pesquisas já concluídas.

---

### 🧭 Roteamento de Diretrizes (Hub de IA)

Para manter o contexto enxuto, livre de redundâncias e focado no domínio, as regras e habilidades de desenvolvimento deste repositório foram totalmente modularizadas. Consulte os links abaixo antes de realizar qualquer tarefa específica:

1. **Segurança e Operação:**
   - **Aprovação de Comandos:** As restrições de execução e segurança no terminal estão descritas em [terminal-approval-flow.md](rules/terminal-approval-flow.md).
   - **Gestão de Segredos:** Diretrizes para proteção de credenciais e uso de secrets locais estão em [secret-management.md](rules/secret-management.md).

2. **Versionamento de Código (Git):**
   - **Nomenclatura de Branches e Fluxo de Merge:** Regras para nomear branches (`<operacao>/<ticket> - <descricao>`) e para o fluxo de integração (branches integram na `develop`; `develop` integra na `main` somente com aprovação do responsável) estão em [branch-and-merge-flow.md](rules/branch-and-merge-flow.md).
   - **Higiene do Git:** Regras para `.gitignore` e arquivos temporários de compilação estão em [git-hygiene.md](rules/git-hygiene.md).
   - **Operação de Versionamento:** O passo a passo de criação de branch, commits e merge está na skill [git-workflow-manager](.agents/skills/git-workflow-manager/SKILL.md).

3. **Especificações de Desenvolvimento (SDD):**
   - **Processo SDD:** A obrigatoriedade de leitura de especificações antes do início da codificação está descrita em [spec-driven-development.md](rules/spec-driven-development.md).
   - **Criação e Formato de Specs:** Regras de nomenclatura e templates obrigatórios de especificação estão delegadas à skill [sdd-spec-enforcer](.agents/skills/sdd-spec-enforcer/SKILL.md).

4. **Tema de Domínio e Regras de Roteamento:**
   - **Contexto de Negócio (MachineReturn):** A especificação de personas, entidades do domínio (classes ricas) e regras de triagem automática estão descritas em [domain-context.md](rules/domain-context.md).

5. **Arquitetura, Banco de Dados, Cache e Testes:**
   - **Arquitetura e Configurações:** A nomenclatura de projetos .csproj, .sln, dependências, resiliência do banco de dados, Redis cache-aside, estratégia de testes (unitários/integração) e testes manuais (.http) estão descritos em [architecture-guide.md](rules/architecture-guide.md).
   - **Estrutura da Solução:** A nomenclatura de projetos e o fluxo de dependências clássicas estão detalhados em [solution-structure.md](rules/solution-structure.md).
   - **Domínio Rico (DDD):** Diretrizes de modelagem rica estão na skill [rich-domain-builder](.agents/skills/rich-domain-builder/SKILL.md).
   - **Fatias Verticais (Vertical Slices):** Padrões para rotas da API, handlers e validações estão na skill [net8-vertical-slice-generator](.agents/skills/net8-vertical-slice-generator/SKILL.md).
   - **Mapeamento e Migrações (EF Core):** Regras Fluent API e migrações estão na skill [efcore-config-migration-enforcer](.agents/skills/efcore-config-migration-enforcer/SKILL.md).
   - **Estratégias de Cache (Redis):** Gerenciamento de chaves e resiliência estão na skill [redis-cache-manager](.agents/skills/redis-cache-manager/SKILL.md).
   - **Testes Unitários:** Stack xUnit, Moq e FluentAssertions na skill [xunit-moq-fluentassertions-tester](.agents/skills/xunit-moq-fluentassertions-tester/SKILL.md).
   - **Testes de Integração:** Testcontainers com PostgreSQL e Redis na skill [testcontainers-integration-tester](.agents/skills/testcontainers-integration-tester/SKILL.md).

Antes de codificar qualquer nova funcionalidade, localize e leia a especificação correspondente (`spec-*.md`) no diretório `/specs`.
