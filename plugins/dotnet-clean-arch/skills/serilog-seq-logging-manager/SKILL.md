---
name: serilog-seq-logging-manager
description: Ativado ao configurar logging estruturado com Serilog, integração de visualização local com Seq via docker-compose e enriquecimento de contexto de rastreamento no .NET 8.
---

# Structured Logging and Observability with Serilog & Seq

Esta habilidade orienta a implementação de logging estruturado (semântico) usando Serilog no .NET 8 e a integração local com o visualizador Seq para depuração rápida e análise de fluxo.

## Configuração do Serilog na API (.NET 8)

Evite hardcoding de configurações. Utilize o arquivo `appsettings.json` para definir níveis de log e destinos (sinks).

1. **Bootstrap e Registro:**
   - Instale os pacotes necessários:
     - `Serilog.AspNetCore`
     - `Serilog.Sinks.Console`
     - `Serilog.Sinks.Seq`
     - `Serilog.Enrichers.Span` (ou use suporte nativo do .NET 8 para TraceIds).
   - Configure o Serilog logo na inicialização do `Program.cs` para capturar falhas de inicialização da API (bootstrap logging).
   - Registre o provedor no host do ASP.NET Core:
     `builder.Host.UseSerilog((context, configuration) => configuration.ReadFrom.Configuration(context.Configuration));`

2. **Configuração via JSON (`appsettings.Development.json`):**
   - Configure o arquivo para habilitar os sinks de Console e Seq localmente:

     ```json
     "Serilog": {
       "Using": [ "Serilog.Sinks.Console", "Serilog.Sinks.Seq" ],
       "MinimumLevel": {
         "Default": "Information",
         "Override": {
           "Microsoft": "Warning",
           "System": "Warning"
         }
       },
       "WriteTo": [
         { "Name": "Console" },
         {
           "Name": "Seq",
           "Args": { "serverUrl": "http://localhost:5341" }
         }
       ],
       "Enrich": [ "FromLogContext", "WithMachineName", "WithThreadId" ]
     }
     ```

## Diretrizes de Logs Estruturados (Semânticos)

Para garantir que as ferramentas de análise consigam indexar e pesquisar propriedades do domínio:

1. **Nunca use Interpolação de Strings para dados variáveis:**
   - **Incorreto:** `_logger.LogInformation($"Máquina {maquina.Codigo} recebida para triagem na fábrica {fabrica.Nome}");` (Gera uma string de texto livre sem propriedades indexáveis).
   - **Correto:** `_logger.LogInformation("Máquina {CodigoMaquina} recebida para triagem na fábrica {NomeFabrica}", maquina.Codigo, fabrica.Nome);` (Cria duas propriedades indexáveis `CodigoMaquina` e `NomeFabrica` no payload JSON enviado ao Seq).

2. **Convenção de Nomenclatura das Propriedades:**
   - Utilize propriedades em formato CamelCase ou PascalCase e seja consistente.
   - Sempre dê nomes específicos aos identificadores do domínio (ex: use `CodigoMaquina` em vez de apenas `Id` ou `Codigo` para evitar colisões ao correlacionar logs de diferentes entidades).

3. **Enriquecimento com Tracing e Contexto:**
   - Garanta que o middleware de log do Serilog (`app.UseSerilogRequestLogging()`) esteja ativado na camada de API. Ele limpa os logs verbosos do ASP.NET padrão e gera uma única entrada rica para cada requisição HTTP.
   - O `TraceId` e `SpanId` gerados pelo .NET são repassados automaticamente nos metadados do log. No Seq, você pode clicar no ícone de Trace para visualizar a sequência de logs associada a uma única requisição.

## Orquestração Local com Seq (Docker Compose)

Para habilitar a visualização e busca local dos logs, inclua o serviço do Seq no arquivo `docker-compose.yml` da raiz do projeto:

```yaml
version: '3.8'

services:
  # ... outros serviços (postgres, redis) ...

  seq:
    image: datalust/seq:latest
    container_name: machinereturn-seq
    environment:
      - ACCEPT_EULA=Y
    ports:
      - "5341:5341" # Porta de Ingestão de Logs (API do Serilog)
      - "8081:80"   # Porta do Dashboard Web (Visualização)
    volumes:
      - seq_data:/data
    restart: unless-stopped

volumes:
  seq_data:
```

Ao rodar os containers, os logs estruturados da API serão ingeridos na porta `5341` e poderão ser consultados de forma avançada acessando `http://localhost:8081` no navegador.
