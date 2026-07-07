# Diretrizes Arquiteturais, de Infraestrutura e Testes

Este documento orienta sobre a arquitetura do sistema, configurações de banco e cache, estratégias de testes e validação manual.

---

## 🏛️ Arquitetura do Sistema

O projeto é estruturado utilizando conceitos de **Clean Architecture** combinados com **Vertical Slice Architecture** distribuídos nas seguintes camadas:

1. **Domain:** Contém as entidades ricas do negócio, agregados e objetos de valor.
   - *Diretriz:* Siga a skill [rich-domain-builder](file:///.agents/skills/rich-domain-builder/SKILL.md) para encapsulamento das invariantes e validações.
2. **Application:** Orquestra os casos de uso do sistema por fatias verticais (features).
   - *Diretriz:* Siga a skill [net8-vertical-slice-generator](file:///.agents/skills/net8-vertical-slice-generator/SKILL.md).
3. **Infra:** Implementa a persistência de dados (PostgreSQL via EF Core) e infraestrutura de cache (Redis).
   - *Diretriz:* Siga a skill [efcore-config-migration-enforcer](file:///.agents/skills/efcore-config-migration-enforcer/SKILL.md) para mapeamento Fluent API e criação de migrações.
   - *Diretriz:* Siga a skill [redis-cache-manager](file:///.agents/skills/redis-cache-manager/SKILL.md) para cache distribuído e estratégias de invalidação.
4. **API:** Camada de entrada (Minimal APIs/Controllers) que expõe os endpoints das fatias verticais.
5. **Shared:** Contém o middleware de tratamento global de exceções para conversão semântica de erros (ex: `DomainException` -> HTTP 400/422).

---

## 💾 Banco de Dados, Cache e Configurações Locais

- **Banco de Dados e Cache:** Utiliza PostgreSQL (persistência de escrita) e Redis (cache distribuído).
  - *Diretriz:* Consulte a skill [redis-cache-manager](file:///.agents/skills/redis-cache-manager/SKILL.md) para detalhes de gerenciamento de chaves e resiliência com Redis.
- **Orquestração Local:** A infraestrutura local é orquestrada via `docker-compose.yml` e arquivos `Dockerfile`.
- **Dados Iniciais (Seeds):** Carga automática no banco de dados para criar um usuário administrador padrão (`admin`).
- **Migrações (EF Core):** As migrações residem na camada `Infra` e devem ser aplicadas automaticamente na inicialização da API em desenvolvimento, conforme detalhado na skill [efcore-config-migration-enforcer](file:///.agents/skills/efcore-config-migration-enforcer/SKILL.md).
- **Resiliência:** Configure políticas de retry como `EnableRetryOnFailure` do EF Core para o PostgreSQL, tolerando atrasos de inicialização dos containers.
- **Segredos e Configurações:** Siga estritamente a regra de segurança descrita em [secret-management.md](file:///mnt/c/Users/jose.dotta/Documents/Projects/SDD-Usage/MachineReturnProto/rules/secret-management.md).

---

## 🧪 Estratégia de Testes

Toda nova funcionalidade criada deve conter testes correspondentes para garantir qualidade de ponta a ponta:

1. **Testes Unitários:** Focados na lógica do Domain e Application de forma isolada.
   - *Diretriz:* Siga a skill [xunit-moq-fluentassertions-tester](file:///.agents/skills/xunit-moq-fluentassertions-tester/SKILL.md).
2. **Testes de Integração:** Fluxos ponta a ponta em banco e cache reais e efêmeros.
   - *Diretriz:* Siga a skill [testcontainers-integration-tester](file:///.agents/skills/testcontainers-integration-tester/SKILL.md).

---

## 📞 Testes Manuais (Arquivos `.http`)

- Para testes manuais rápidos na API, crie arquivos com extensão `.http` na camada de API ou no diretório `/requests` na raiz do projeto.
- **Regra:** Crie um arquivo `.http` individual para cada seção de domínio ou Aggregate Root (ex: `requests/machine-returns.http`) para manter os testes focados por contexto.
