# Spec-Driven Development (SDD) & AI Task Harness

Você deve seguir o fluxo de Spec-Driven Development para todas as tarefas de implementação e modificação de código neste projeto, guiado pela estrutura de harness de tarefas de IA.

## 🔄 Fluxo de Tasks de IA (3 Steps)

Toda tarefa de IA neste projeto deve seguir rigorosamente um ciclo de vida composto por 3 fases sequenciais gerenciadas pelo harness em `scripts/task.sh`:

1. **Research (Pesquisa):**
   - **Objetivo:** Explorar o codebase, identificar dependências, mapear arquivos a modificar/criar e analisar potenciais impactos.
   - **Validação Humana:** Obrigatória antes de prosseguir. O agente deve preencher a seção correspondente no arquivo de task e solicitar a validação.
2. **Plan (Planejamento):**
   - **Objetivo:** Desenhar a solução técnica e **gerar obrigatoriamente o Spec file** (`specs/spec-*.md`) documentando as especificações da funcionalidade.
   - **Validação Humana:** Obrigatória antes de prosseguir. A aprovação da fase de Plan exige que o arquivo Spec seja gerado e seu caminho seja corretamente apontado no harness de tasks.
3. **Implement (Implementação):**
   - **Objetivo:** Codificar as alterações, escrever testes unitários/integração, garantir que o build e os testes passam, e rodar linters.
   - **Validação Humana:** Obrigatória para concluir a task.

---

## Regras de Desenvolvimento

1. **Leitura Obrigatória:** Antes de iniciar a implementação ou modificação de qualquer código, você DEVE localizar e ler o arquivo de especificação correspondente (`spec-*.md` na pasta `/specs`).
2. **Fidelidade às Specs:** Toda implementação deve seguir estritamente as regras de negócio, contratos de API e critérios de aceitação descritos na especificação.
3. **Sem Adivinhações:** Não invente, assuma ou adicione comportamentos/regras que não estejam explicitamente documentados na especificação correspondente.

---

## Formatação e Validação das Specs (Markdown)

1. **Padrão Estético de Referência:** Toda especificação criada ou editada deve seguir a estrutura e formatação visual exemplificada no arquivo de exemplo [spec-example.md](specs/spec-example.md).
2. **Estrutura de Cenários BDD:** Conforme os padrões de IA-Native do projeto, todas as regras de aceitação de uma especificação devem ser estruturadas em cenários BDD formais usando as marcações **Dado / Quando / Então** (Given / When / Then), garantindo clareza técnica e facilidade para testes automatizados.
3. **Automação do Linter:** A formatação estética (como linhas em branco e recuos) é tratada automaticamente. Antes de enviar alterações, execute a validação e correção automática através do comando:

   ```bash
   npx markdownlint-cli --fix --disable MD013 <caminho-do-arquivo-ou-pasta>
   ```

---

## Modificações de Regras e Habilidades de IA (Rules e Skills)

> [!IMPORTANT]
> **Regra Geral aos Agentes de IA:** Qualquer alteração de configuração de IA, regra (rule) ou habilidade (skill) neste repositório deve ser realizada nos seguintes diretórios na raiz do projeto:
>
> - Regras (*rules*): na pasta `rules/`
> - Habilidades (*skills*): na pasta `.agents/skills/`
>
> Não utilize mais comandos do Tessl (como `tessl install` ou `tessl doctor`), pois o Tessl foi removido do projeto.
