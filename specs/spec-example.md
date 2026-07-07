---
id: SPEC-EXAMPLE-01
feature: Example Feature
pod: Core
priority: High
iteration: Sprint 1
contract: OpenAPI
---

# Example Feature Specification

## User Value

As a user, I want to have a clear example of a specification document so that I can write valid Markdown files.

## Acceptance Criteria

### Cenário 1: Formatação do documento e recuo de listas

Dado que uma especificação técnica está sendo escrita em Markdown
Quando o linter de documentação é executado sobre o arquivo
Então o arquivo deve seguir as regras de formatação descritas abaixo:

* O documento deve estar em conformidade estética com as regras markdownlint.
* Blocos de código devem ter linhas em branco acima e abaixo deles.
* Itens de lista aninhados devem respeitar a indentação recomendada (ex: 3 espaços para o primeiro nível de aninhamento).

## Data Model

```json
{
  "exampleId": "SPEC-01",
  "status": "Draft"
}
```

## Security Constraints

Access should be limited to authorized developers only.

## API Contract

The API contract is defined in the Swagger file.

## Dependencies

None.

## Out of Scope

Implementation details are out of scope.
