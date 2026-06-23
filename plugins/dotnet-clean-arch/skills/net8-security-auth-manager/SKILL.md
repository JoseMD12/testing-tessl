---
name: net8-security-auth-manager
description: Ativado ao configurar a autenticação e autorização (JWT Bearer, Roles e Políticas de Acesso) nas fatias verticais da camada de API do .NET 8.
---

# Authentication and Authorization (Security Manager)

Esta habilidade orienta a implementação segura de controle de acesso na API do .NET 8, definindo padrões de segurança com JWT (JSON Web Tokens), mapeamento de perfis (Roles) de usuários e abstração de contexto do usuário logado para evitar acoplamento da infraestrutura com o domínio.

## Autenticação com JWT Bearer

Para garantir a identidade dos usuários que interagem com endpoints restritos (como Agentes de Qualidade):

1. **Configuração do Token:**
   - Utilize a autenticação baseada em JWT Bearer padrão do ASP.NET Core (`Microsoft.AspNetCore.Authentication.JwtBearer`).
   - Todos os parâmetros sensíveis de validação do token (Chave Secreta, Issuer, Audience, tempo de expiração) devem ser configurados no `appsettings.json` e carregados de forma segura, seguindo as diretrizes descritas em [secret-management.md](file:///mnt/c/Users/jose.dotta/Documents/Projects/SDD-Usage/MachineReturnProto/plugins/dotnet-clean-arch/rules/secret-management.md).
   - Registre os serviços de autenticação no `Program.cs`:

     ```csharp
     builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
         .AddJwtBearer(options => { ... });
     ```

2. **Endpoints Públicos vs Protegidos:**
   - Rotas de livre acesso (ex: abertura de chamado por Consumidores sem login) devem ser marcadas explicitamente com o atributo `[AllowAnonymous]` ou não possuir filtros de restrição.
   - Rotas restritas devem ser protegidas pelo middleware de autorização (`app.UseAuthorization()`).

## Autorização Baseada em Roles e Políticas

Diferencie as permissões das personas do sistema para proteger operações administrativas:

1. **Roles do Sistema:**
   - O sistema possui papéis definidos como `AgenteQualidade`.
   - Aplique restrições diretamente nos endpoints das fatias verticais (Minimal APIs ou Controllers) usando atributos de autorização:
     - `[Authorize(Roles = "AgenteQualidade")]`

2. **Políticas Customizadas (Optional):**
   - Para regras de autorização mais granulares, utilize políticas baseadas em Claims (ex: `builder.Services.AddAuthorization(options => options.AddPolicy("ApenasFábricaNacional", policy => ...))`).

## Abstração de Contexto do Usuário (IUserContext)

Nunca injete o `HttpContext` ou trabalhe diretamente com `ClaimsPrincipal` dentro dos Handlers da camada de `Application` ou entidades do `Domain` (para evitar violações das regras de Clean Architecture):

1. **Interface de Abstração:**
   - Defina uma interface simples na camada de `Application` (ex: `IUserContext` ou `ICurrentUserService`):

     ```csharp
     public interface IUserContext
     {
         string? UserEmail { get; }
         string? Role { get; }
         bool IsAuthenticated { get; }
     }
     ```

2. **Implementação na API/Infra:**
   - Implemente esta interface na camada de `API` ou `Infra` utilizando o `IHttpContextAccessor` nativo do ASP.NET Core para ler as claims do token decodificado:

     ```csharp
     public class UserContext : IUserContext
     {
         private readonly IHttpContextAccessor _httpContextAccessor;
         // ... ler as claims do _httpContextAccessor.HttpContext?.User ...
     }
     ```

   - Registre o serviço na DI: `builder.Services.AddScoped<IUserContext, UserContext>();`.
   - Injete a interface `IUserContext` nos Command e Query Handlers da camada de `Application` para validar a identidade do usuário executor da ação.

## Dados Iniciais (Seeds) e Carga de Perfis

- Ao inicializar o banco de dados em ambiente de desenvolvimento, certifique-se de realizar a carga inicial automática (seeding) de perfis (Roles) e de um usuário padrão de administração (ex: `admin`), conforme descrito em `AGENTS.md`.
