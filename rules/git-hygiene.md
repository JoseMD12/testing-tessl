# Git Hygiene

Manutenção de higiene de arquivos no Git para o repositório.

## Regras do Git

- **Exclusões no .gitignore:** Garanta que todos os arquivos temporários, de compilação ou de runtime não sejam commitados.
- **Pastas do Compilador .NET:** Excluir recursivamente pastas `bin/` e `obj/`.
- **Arquivos e Pastas de IDEs/Editores:** Excluir configurações específicas de usuário e pastas como `.vs/`, `.idea/`, arquivos `.user`.
- **Harness de Tasks:** O arquivo de ponteiro ativo do harness de tasks `tasks/.active` deve permanecer fora do controle de versão (já configurado no `.gitignore`).
- **Verificação:** Antes de fazer commits, sempre execute `git status` para certificar-se de que nenhum desses arquivos ou diretórios está sendo rastreado pelo Git.
