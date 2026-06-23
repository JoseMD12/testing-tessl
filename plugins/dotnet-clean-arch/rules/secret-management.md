# Secret Management

Segurança e governança de dados sensíveis e credenciais.

## Regras de Segurança

- **Nunca** exponha ou envie por commit credenciais, chaves de API, senhas, strings de conexão ou segredos de banco de dados no repositório de controle de versão (Git).
- **Desenvolvimento Local:** Use a ferramenta `dotnet user-secrets` do .NET para gerenciar configurações e segredos confidenciais em sua máquina local.
- **Produção e Containers:** Utilize variáveis de ambiente (Environment Variables) passadas via Docker, Kubernetes ou serviços de nuvem para injetar segredos.
- **Arquivos de Configuração:** Mantenha arquivos como `appsettings.json` apenas com placeholders ou configurações públicas/não-sensíveis.
