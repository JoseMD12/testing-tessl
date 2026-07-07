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

1. The document must be written in Markdown.
2. List items must follow spacing rules:
   * First nested list item with 3 spaces indentation.
   * Second nested list item with 3 spaces indentation:
     * Deeply nested item with 5 spaces indentation under its parent.
3. Blocks of code must have blank lines around them.

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
