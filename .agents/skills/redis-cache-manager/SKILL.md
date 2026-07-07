---
name: redis-cache-manager
description: Ativado ao implementar cache distribuído no Redis, manipulação de cache-aside, definição de chaves (Key Management) e invalidação de cache na camada de Application e Infraestrutura do .NET 8.
---

# Redis Cache Manager

Esta habilidade orienta a implementação e o gerenciamento de cache distribuído usando Redis no .NET 8, focando no desacoplamento da infraestrutura, estratégias eficientes de leitura/escrita e resiliência a falhas do serviço de cache.

## Abstração e Desacoplamento

Para manter a integridade da arquitetura limpa (Clean Architecture), evite acoplar a lógica de domínio ou aplicação diretamente a bibliotecas de terceiros (como StackExchange.Redis):

1. **Interface de Acesso:**
   - Utilize a abstração nativa do .NET `IDistributedCache` ou crie uma interface própria (`ICacheService`) na camada de `Application`.
   - Implemente a persistência e conexão física com o Redis na camada de `Infra`.

2. **Serialização de Dados:**
   - Armazene dados estruturados no Redis preferencialmente serializados em formato JSON (utilizando `System.Text.Json`).
   - Garanta que as classes serializadas possuam construtores adequados para desserialização (evitando falhas em propriedades com setters privados de classes ricas).

## Gerenciamento de Chaves (Key Management)

Para evitar colisões e manter o Redis organizado, utilize chaves estruturadas e hierárquicas:

1. **Padrão de Chave:**
   - O formato padrão deve ser: `nomedoapp:contexto:identificador` (usando `:` como delimitador).
   - Exemplo para máquina: `machinereturn:maquinas:MQ-9988`
   - Exemplo para chamado: `machinereturn:chamados:77c2bb0e`

2. **Constantes e Helpers:**
   - Defina as chaves ou padrões de chaves em constantes ou classes auxiliares na camada de `Application` para evitar duplicação de strings mágicas no código.

## Estratégias de Cache e Invalidação

A manipulação de dados em cache deve seguir regras claras de leitura e ciclo de vida:

1. **Padrão Cache-Aside (Leitura):**
   - Sempre tente ler do Redis primeiro.
   - Em caso de Cache Hit: Retorne o valor desserializado diretamente do cache.
   - Em caso de Cache Miss: Busque as informações no banco de dados relacional (PostgreSQL), salve no Redis e depois retorne os dados.

2. **Invalidação Ativa (Escrita/Mutação):**
   - Sempre que uma entidade for alterada no banco de dados (inserção, atualização ou exclusão), a respectiva chave de cache no Redis deve ser invalidada imediatamente (`RemoveAsync`) para evitar o consumo de dados desatualizados.
   - Em operações em lote, limpe as chaves associadas ou invalide a coleção correspondente.

3. **Ciclo de Vida (TTL - Time to Live):**
   - Sempre configure um tempo de expiração para os dados gravados no Redis usando `DistributedCacheEntryOptions`.
   - Utilize `AbsoluteExpirationRelativeToNow` (tempo máximo de permanência, ex: 1 hora) para garantir que dados novos entrem eventualmente.
   - Opcionalmente, use `SlidingExpiration` (expira se não for acessado por um período, ex: 15 minutos).

## Resiliência e Fallback

O cache deve ser tratado como um acelerador de performance secundário. A indisponibilidade do Redis nunca deve derrubar o funcionamento principal da API:

1. **Tolerância a Falhas (Fault Tolerance):**
   - Envolva as chamadas de leitura/escrita do Redis em blocos try-catch para capturar falhas transientes de conexão do cache.
   - Em caso de exceção de conexão com o Redis, logue um aviso (`LogWarning`) e realize o fallback silencioso executando a consulta diretamente no banco de dados (PostgreSQL).
