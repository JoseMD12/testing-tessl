---
name: sdd-spec-enforcer
description: Triggered when managing, creating or validating feature specifications (specs) in spec-*.md
---

# SDD Spec Enforcer

Cada caso de uso (feature) do sistema deve ser guiado por especificações documentadas. Siga rigorosamente as diretrizes abaixo:

## Nomenclatura das Specs

Cada especificação de caso de uso deve ser definida em um arquivo Markdown no formato:
`spec-<dominio/contexto>-<numero_feature>-<nome_feature>.md` (ex: `spec-machine-returns-01-abrir-chamado.md`).

## Localização

As especificações ficam armazenadas na pasta `/specs` ou `/docs/specs` na raiz do projeto.

## Processo Operacional de Criação da Spec

Ao receber a tarefa de mapear uma nova especificação, você deve agir como um Analista de Sistemas:

1. Fase de Entrevista: Formule de 3 a 5 perguntas claras ao usuário humano para sanar dúvidas sobre regras de negócio específicas da funcionalidade, limites do domínio e payload esperado.
2. Geração do Rascunho: Preencha o template obrigatório abaixo salvando o arquivo na pasta correta.
3. Ponto de Parada: Avise o usuário no chat que a especificação foi rascunhada e aguarde o sinal verde ("Aprovado", "Pode codificar") antes de prosseguir para qualquer etapa de desenvolvimento técnico (.NET 8).

## Formato Obrigatório de Spec

Cada arquivo de especificação deve seguir rigorosamente o seguinte template:

```markdown
id: <ID_DA_SPEC>
feature: <NOME_DA_FEATURE>
pod: <POD_OU_DOMINIO>
priority: <PRIORIDADE>
iteration: <ITERACAO_E_PRAZO>
contract: <CONTRATO_OPCIONAL_OU_OPENAPI>

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
