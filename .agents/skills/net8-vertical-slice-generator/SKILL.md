---
name: net8-vertical-slice-generator
description: Ativado ao criar uma nova funcionalidade seguindo a arquitetura de fatias verticais (Vertical Slices) nas camadas API e Application do .NET 8.
---

# .NET 8 Vertical Slice Generator

Esta habilidade orienta a criação e o scaffolding de novas funcionalidades (features) seguindo a arquitetura de fatias verticais (Vertical Slices) nas camadas de API e Application do .NET 8.

## Diretrizes de Implementação

1. **Foco e Coesão (Vertical Slice):** Cada funcionalidade deve encapsular todas as suas peças (Request, Command/Query, Handler, Validator, Response) em uma única pasta dedicada na camada `Application` (ex: `Application/Features/Chamados/AbrirChamado/`).
2. **Camada de API:**
   - **Regra Absoluta:** O projeto `MachineReturn.API` deve utilizar exclusivamente **Minimal APIs nativas do .NET 8** (criado com `dotnet new webapi --use-controllers false`). A utilização de Controllers clássicos é estritamente proibida no ecossistema deste projeto.
   - O mapeamento de endpoints deve ocorrer de forma descentralizada e fluida junto às fatias verticais.
   - Injete o Mediador (MediatR) para encaminhar o Request ao Handler correspondente.
3. **Validação de Entrada:**
   - Implemente validações robustas usando FluentValidation se necessário, encapsuladas na mesma pasta da Feature.
4. **Semântica e Erros:**
   - Evite try-catch genérico na camada de API ou Application. Confie no middleware global de exceções na camada `Shared` que captura `DomainException` e retorna os status HTTP adequados (`400 Bad Request`, `422 Unprocessable Entity`).
5. **Código de Exemplo/Estrutura:**
   - Cada Feature deve expor classes específicas:
     - `public record Command(...) : IRequest<Result>;`
     - `public class Validator : AbstractValidator<Command> { ... }`
     - `public class Handler : IRequestHandler<Command, Result> { ... }`
6. **Regras de Negócio da Feature (SDD):**
   - A lógica implementada dentro de cada Handler ou Validator deve seguir estritamente as regras de negócio e critérios de aceitação definidos no arquivo de especificação (`spec-*.md`) da respectiva funcionalidade.
