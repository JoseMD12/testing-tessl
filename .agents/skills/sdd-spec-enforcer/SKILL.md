---
name: sdd-spec-enforcer
description: Triggered when managing, creating or validating feature specifications (specs) in spec-*.md
---

# SDD Spec Enforcer

Cada caso de uso (feature) do sistema deve ser guiado por especificações documentadas. No contexto do harness de tasks, a especificação DEVE ser gerada durante a fase de **Plan (Planejamento)**. Siga rigorosamente as diretrizes abaixo:

## Nomenclatura das Specs

Cada especificação de caso de uso deve ser definida em um arquivo Markdown no formato:
`spec-<dominio/contexto>-<numero_feature>-<nome_feature>.md` (ex: `spec-machine-returns-01-abrir-chamado.md`).

## Localização

As especificações ficam armazenadas na pasta `/specs` na raiz do projeto.

## Processo Operacional de Criação da Spec (Fase de Plan)

Ao receber a tarefa de mapear uma nova especificação durante a fase de Plan:

1. **Fase de Entrevista:** Formule de 3 a 5 perguntas claras ao usuário humano para sanar dúvidas sobre regras de negócio específicas da funcionalidade, limites do domínio e payload esperado.
   - **Nota sobre Ambientes de Avaliação / Não-Interativos:** Se você estiver rodando em um ambiente de teste automatizado (CI ou qualquer execução não-interativa onde o usuário físico não possa responder), pule a fase de entrevista gerando respostas padrão plausíveis e prossiga diretamente.
2. **Geração do Rascunho:** Preencha o template obrigatório abaixo salvando o arquivo na pasta `/specs`.
3. **Ponto de Parada & Validação da Task:** Insira o caminho do Spec gerado no arquivo de task ativo (ex: `Path: specs/spec-*.md`) e peça para o usuário validar esta fase rodando o script de aprovação do harness:
   ```bash
   ./scripts/task.sh approve
   ```
   - **Nota sobre Ambientes de Avaliação / Não-Interativos:** Se estiver em um ambiente automatizado sem interação com usuário físico (onde você deve executar as tarefas de ponta a ponta sem parar), pule este ponto de parada e continue o desenvolvimento técnico com base no rascunho de especificação gerado.

## Formato Obrigatório de Spec

Cada arquivo de especificação deve seguir rigorosamente o seguinte template:

```markdown
---
id: <ID_DA_SPEC>
feature: <NOME_DA_FEATURE>
pod: <POD_OU_DOMINIO>
priority: <PRIORIDADE>
iteration: <ITERACAO_E_PRAZO>
contract: <CONTRATO_OPCIONAL_OU_OPENAPI>
---

# <Título da Spec>

## User Value
<Descrição do valor para o usuário/negócio>

## Acceptance Criteria
<Lista numerada de critérios de aceitação e contratos de rotas>

## Data Model
<Entidades e estruturas de dados associadas>

## Security Constraints
<Restrições de segurança, autenticação, lints de entrada e tratamento de PII>

## API Contract
<Referência ao contrato formal como OpenAPI ou gRPC>

## Dependencies
<Dependências ou serviços bloqueantes>

## Out of Scope
<O que está expressamente fora do escopo desta especificação>
```

