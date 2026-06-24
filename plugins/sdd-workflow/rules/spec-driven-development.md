# Spec-Driven Development (SDD)

Você deve seguir o fluxo de Spec-Driven Development para todas as tarefas de implementação e modificação de código neste projeto.

## Regras de Desenvolvimento

1. **Leitura Obrigatória:** Antes de propor ou implementar qualquer alteração de código, criação de arquivos, banco de dados ou testes, você DEVE localizar e ler o arquivo de especificação da feature correspondente (`spec-*.md` na pasta `/specs` ou `/docs/specs`).
   - Exceção: Se a tarefa atribuída a você for justamente a criação ou escrita de uma nova especificação, ignore a leitura obrigatória e acione imediatamente a skill sdd-spec-enforcer.
2. **Fidelidade às Specs:** Toda implementação deve seguir estritamente as regras de negócio, contratos de API e critérios de aceitação descritos na especificação.
3. **Sem Adivinhações:** Não invente, assuma ou adicione comportamentos/regras que não estejam explicitamente documentados na especificação correspondente.

## Regras de Formatação e Escrita de Markdown (Linting)

Ao criar ou editar qualquer arquivo Markdown no projeto (incluindo especificações e documentações), siga rigorosamente os padrões de estilo abaixo para garantir a conformidade com as regras de linting:

1. **Espaçamento de Cabeçalhos (Headers):**
   - Sempre insira uma linha em branco **antes** e **depois** de qualquer cabeçalho markdown (`#`, `##`, `###`).
2. **Sem Dois-Pontos no Final de Títulos:**
   - Nunca termine um cabeçalho ou título com dois-pontos (`:`).
3. **Indentação de Listas Não Ordenadas (MD007/ul-indent):**
   - Use exatamente **2 espaços** de recuo/indentação para listas não ordenadas aninhadas (sub-itens), mantendo a consistência em todo o documento.
4. **Espaçamento ao Redor de Listas (MD032/blanks-around-lists):**
   - Toda lista (ordenada ou não ordenada) deve ser obrigatoriamente precedida e sucedida por uma linha em branco.
5. **Espaçamento ao Redor de Blocos de Código (MD031/blanks-around-fences):**
   - Todos os blocos de código (fenced code blocks) devem ser obrigatoriamente cercados por uma linha em branco (tanto **antes** do início quanto **depois** do fechamento).
   - Especifique sempre a linguagem no bloco (ex: ` ```csharp ` ou ` ```json `).
