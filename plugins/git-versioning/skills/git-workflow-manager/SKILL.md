---
name: git-workflow-manager
description: Triggered when creating branches, committing, or integrating code via Git (branch naming, merge flow into develop/main)
---

# Git Workflow Manager

Esta skill define o passo a passo operacional para versionar código com Git neste projeto, garantindo nomenclatura de branches consistente e um fluxo de merge controlado.

## Criação de Branch

1. **Parta sempre da `develop`:** Antes de iniciar qualquer alteração, atualize a branch `develop` e crie a nova branch a partir dela.

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feat/MR-123-create-return-request
   ```

2. **Siga a nomenclatura obrigatória:** O nome da branch segue o formato conceitual `<operacao>/<ticket> - <descricao geral>`, materializado em *kebab-case* (`<operacao>/<ticket>-<descricao-geral>`) por causa da restrição do Git a espaços, conforme a regra `branch-and-merge-flow.md`.
3. **Prefixos de operação aceitos:** `feat`, `fix`, `refac`, `doc`, `test`, `chore`.

## Commits

1. **Mensagens claras e no escopo:** Escreva mensagens de commit curtas e descritivas, idealmente alinhadas ao prefixo de operação da branch (ex: `feat: create return request`).
2. **Higiene antes do commit:** Execute `git status` e confirme que nenhum artefato de build, IDE ou runtime (`bin/`, `obj/`, `.vs/`, `.idea/`, `.tessl/`) está sendo rastreado, conforme a regra `git-hygiene.md`.

## Fluxo de Merge

1. **Branch de trabalho para `develop`:** Abra um Pull Request com a `develop` como branch de destino. Toda branch de operação integra exclusivamente na `develop`.
2. **Nunca abra PR de branch de trabalho para `main`:** A `main` não recebe merges diretos de branches de trabalho.
3. **`develop` para `main` somente com aprovação:** A promoção de `develop` para `main` só ocorre quando a versão for explicitamente aprovada pelo responsável pelo projeto. Não realize esse merge sem a aprovação explícita.

## Checklist Final

- A branch foi criada a partir da `develop` e segue a nomenclatura obrigatória.
- O Pull Request aponta para a `develop` como destino (nunca `main`).
- Nenhum artefato indevido está sendo versionado (`git status` limpo).
- A promoção para `main` aguarda aprovação explícita do responsável.
