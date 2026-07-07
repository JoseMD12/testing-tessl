---
name: net8-error-handling-enforcer
description: Ativado ao implementar o middleware de tratamento global de exceções, validações com FluentValidation e mapeamento de respostas semânticas usando RFC 7807 (Problem Details) no .NET 8.
---

# Global Error Handling and Semantic Validation

Esta habilidade orienta a padronização do tratamento de erros e exceções na camada de API do .NET 8, assegurando que o cliente receba respostas semânticas, estruturadas e consistentes com o padrão da indústria **RFC 7807 (Problem Details)**.

## Diretrizes de Resposta HTTP Semântica

Para evitar o vazamento de stack traces e manter a consistência de comunicação com consumidores externos:

1. **Uso de Problem Details (RFC 7807):**
   - Todas as respostas de erro (HTTP >= 400) devem retornar um payload estruturado utilizando a classe nativa do ASP.NET Core `Microsoft.AspNetCore.Mvc.ProblemDetails`.
   - Propriedades obrigatórias no payload de erro:
     - `Type`: URI que identifica o tipo de erro (ex: `https://tools.ietf.org/html/rfc7231#section-6.5.1`).
     - `Title`: Uma descrição curta e legível por humanos do tipo de erro (ex: "Validation error" ou "Business rule violation").
     - `Status`: O código de status HTTP correspondente.
     - `Detail`: Explicação detalhada do erro ocorrido no contexto específico.
     - `Instance`: URI que identifica a requisição específica (ex: o caminho da rota HTTP acessada).

2. **Tradutor de Exceções de Domínio (HTTP 400 ou 422):**
   - Exceções do tipo `DomainException` (lançadas para proteger invariantes no modelo rico) devem ser capturadas pelo middleware global e traduzidas para:
     - **HTTP 400 (Bad Request)** ou **HTTP 422 (Unprocessable Entity)**, a depender da severidade da violação de negócio.
     - O campo `Detail` deve conter a mensagem de erro encapsulada na exceção de domínio.

3. **Tradutor de Erros de Validação (HTTP 400):**
   - Exceções de validação de payload disparadas pela camada de aplicação (ex: `ValidationException` do `FluentValidation`) devem ser convertidas para **HTTP 400 (Bad Request)**.
   - O payload deve estender a estrutura básica do `ProblemDetails` para incluir um dicionário `Errors` (ex: utilizando `HttpValidationProblemDetails`), onde:
     - As chaves representam o nome da propriedade/campo que falhou.
     - Os valores são uma coleção das mensagens de validação associadas àquele campo específico.

## Implementação do Middleware Global

No .NET 8, utilize a nova interface `IExceptionHandler` em vez de criar middlewares personalizados complexos do zero.

1. **Implementação da Classe de Exceção:**
   - Crie uma classe que implemente `IExceptionHandler` (ex: `GlobalExceptionHandler` na camada de `API` ou `Shared`).
   - Implemente o método `TryHandleAsync` mapeando de forma condicional cada tipo de exceção para sua respectiva resposta semântica.
   - Sempre utilize injeção de dependência para injetar o `ILogger` nesta classe e registrar o erro estruturado antes de responder ao cliente.

2. **Registro e Uso no Program.cs:**
   - Registre o handler de exceção no contêiner de DI:
     `builder.Services.AddExceptionHandler<GlobalExceptionHandler>();`
   - Configure o comportamento padrão para incluir os detalhes do problema em desenvolvimento:
     `builder.Services.AddProblemDetails();`
   - Ative o middleware no pipeline HTTP:
     `app.UseExceptionHandler();`
