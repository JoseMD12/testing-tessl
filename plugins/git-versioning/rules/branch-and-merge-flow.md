# Nomenclatura de Branches e Fluxo de Merge

Todas as alterações de código neste projeto devem ser versionadas em branches dedicadas, seguindo a nomenclatura e o fluxo de integração descritos abaixo.

## Nomenclatura Obrigatória de Branches

Toda branch de trabalho deve ser criada a partir da branch `develop` e nomeada no formato conceitual:

`<operacao>/<ticket> - <descricao geral>`

Como o Git não permite espaços em nomes de branch, o formato deve ser materializado em *kebab-case* (minúsculas, palavras separadas por hífen), preservando a `<operacao>` e o `<ticket>`:

`<operacao>/<ticket>-<descricao-geral>`

Onde:

- **operacao:** Tipo da operação realizada. Use prefixos curtos e consistentes, por exemplo: `feat` (nova funcionalidade), `fix` (correção), `refac` (refatoração), `doc` (documentação), `test` (testes), `chore` (manutenção).
- **ticket:** Identificador do ticket/issue relacionado (ex: `MR-123`). Caso não exista um ticket formal, utilize um identificador descritivo curto.
- **descricao geral:** Resumo curto do que será feito na branch, escrito **obrigatoriamente em inglês**, em *kebab-case* e sem acentos.

Exemplos válidos:

- Conceitual `feat/MR-123 - create return request` resulta na branch `feat/MR-123-create-return-request`.
- `fix/MR-204-fix-consumer-email-validation`
- `refac/MR-310-refactor-factory-triage-rules`
- `doc/MR-045-document-quality-inspection-flow`

## Fluxo de Integração (Merge)

1. **Branches de trabalho sempre integram na `develop`:** Toda branch de operação (`feat/`, `fix/`, `refac/`, etc.) deve ser mergeada exclusivamente na branch `develop` por meio de Pull Request. Nunca faça merge de uma branch de trabalho diretamente na `main`.
2. **`develop` integra na `main` apenas com aprovação do responsável:** A branch `develop` só pode ser mergeada na `main` quando a versão for explicitamente aprovada pelo responsável pelo projeto (o owner). Não promova `develop` para `main` sem essa aprovação explícita.
3. **`main` representa versões aprovadas:** A branch `main` deve conter somente versões revisadas e aprovadas, mantendo-se estável e pronta para entrega.

## Verificações Antes de Abrir um Pull Request

- Confirme que a branch foi criada a partir da `develop` e segue a nomenclatura obrigatória.
- Garanta que o Pull Request tem a `develop` como branch de destino (base).
- Não abra Pull Requests de branches de trabalho diretamente para a `main`.
