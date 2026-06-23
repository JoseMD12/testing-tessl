---
name: efcore-config-migration-enforcer
description: Ativado ao configurar classes de entidade no DbContext (Entity Configuration) ou criar e aplicar migrações (EF Core Migrations) na camada de Infraestrutura do .NET 8.
---

# EF Core Configuration and Migration Enforcer

Esta habilidade orienta a configuração do Entity Framework Core (EF Core) no .NET 8, focando em boas práticas de isolamento de mapeamento de entidades (Fluent API), suporte a modelos de domínio ricos do DDD e governança na criação e execução de migrações.

## Mapeamento de Entidades

Para garantir que o domínio rico e o encapsulamento não sejam comprometidos pela persistência, siga as diretrizes abaixo:

1. **Configurações Isoladas (Fluent API):**
   - Nunca configure mapeamentos inline no método `OnModelCreating` do `DbContext`.
   - Crie uma classe separada para cada entidade implementando `IEntityTypeConfiguration<TEntity>` na camada de `Infra`.
   - Exemplo: `public class MaquinaConfiguration : IEntityTypeConfiguration<Maquina> { ... }`.
   - Registre todas as configurações de uma vez usando `builder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly())` no DbContext.

2. **Persistência de Propriedades com Encapsulamento:**
   - Para propriedades com setters privados ou protegidos (`{ get; private set; }`), o EF Core é capaz de ler e escrever diretamente nos campos ou propriedades de apoio automaticamente.
   - Garanta que propriedades de coleção sejam mapeadas usando campos de apoio (backing fields) se forem expostas como somente leitura (`IReadOnlyCollection<TEntity>`).

3. **Mapeamento de Value Objects:**
   - **Propriedades Únicas Simples:** Utilize Value Converters (`HasConversion`) para mapear Value Objects simples que contêm um único valor para tipos primitivos no banco de dados.
   - **Value Objects Compostos:** Use `.OwnsOne()` ou `.OwnsMany()` para Value Objects com múltiplos atributos, garantindo que suas colunas sejam criadas na mesma tabela da entidade principal ou em tabelas associadas.

4. **Chaves e Índices:**
   - Configure as chaves primárias explicitamente com `.HasKey(...)`.
   - Defina índices únicos com `.HasIndex(...)` para propriedades de negócio que representam identificadores exclusivos (como código da máquina, e-mail do usuário ou número de série).

## Migrações do EF Core

A geração de migrações deve seguir um fluxo controlado para evitar alterações destrutivas acidentais ou migrações vazias:

1. **Compilação do Projeto:**
   - Certifique-se de compilar o projeto (`dotnet build`) com sucesso antes de tentar gerar uma nova migração.

2. **Comando de Migração e Nomenclatura:**
   - O nome da migração passado para o comando deve seguir estritamente o padrão: `v<numero_da_migration>_<nome_da_entidade_ou_agregador>_<acao_resumida>`.
   - Exemplos de nome de migração:
     - `v1_usuario_criar` (gerando o arquivo físico `20260623163330_v1_usuario_criar.cs`)
     - `v2_usuario_adicionar_criptografia` (gerando o arquivo físico `20260624155522_v2_usuario_adicionar_criptografia.cs`)
   - Execute o comando da CLI do EF Core especificando explicitamente o projeto de infraestrutura (onde reside o DbContext) e o projeto de inicialização/API.
   - Exemplo de comando no terminal:
     `dotnet ef migrations add v1_usuario_criar --project src/MachineReturn.Infra --startup-project src/MachineReturn.API`

3. **Revisão da Migração Gerada:**
   - Inspecione a classe de migração gerada (`xxxx_NomeDaMigracao.cs`) e o arquivo snapshot do modelo.
   - Garanta que não existam operações vazias de alteração de banco sem justificativa.
   - Preste atenção especial a operações de remoção de colunas ou tabelas (`DropColumn`, `DropTable`) para evitar perda de dados em ambientes de staging/produção.

4. **Resiliência na Conexão:**
   - No método de configuração do DbContext (dentro da injeção de dependência na camada de infraestrutura ou API), sempre utilize a política de retentativa padrão do provedor do banco de dados (ex: `EnableRetryOnFailure` para PostgreSQL).
   - Isso evita falhas de inicialização do app quando os containers do banco de dados ainda estão subindo.

5. **Aplicação de Migrações em Desenvolvimento:**
   - Em ambiente de desenvolvimento local, aplique as migrações automaticamente ao inicializar a aplicação utilizando `context.Database.Migrate()`.
   - Adicione tratamento de exceções com retentativas na inicialização para lidar com a latência de subida do container do banco de dados.
