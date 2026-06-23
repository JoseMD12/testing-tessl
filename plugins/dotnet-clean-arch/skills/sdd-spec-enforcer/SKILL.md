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

## Uso pela IA
Antes de implementar qualquer código, você deve ler a especificação da feature correspondente para garantir que todas as regras de negócio e contratos descritos na spec sejam rigorosamente seguidos.

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
