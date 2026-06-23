---
name: testcontainers-integration-tester
description: Ativado ao configurar ou modificar testes de integração de banco de dados e cache usando Testcontainers (PostgreSQL e Redis) + xUnit + FluentAssertions.
---

# Integration Testing with Testcontainers

Esta habilidade orienta a criação e manutenção de testes de integração de ponta a ponta que utilizam instâncias de banco de dados e cache reais e efêmeras.

## Diretrizes de Testes de Integração:
1. **Stack de Integração:**
   - **Banco de Dados:** PostgreSQL instanciado via Testcontainers.
   - **Cache:** Redis instanciado via Testcontainers.
   - **Test Runner & Assertions:** xUnit + FluentAssertions.
2. **Isolamento Total de Banco de Dados:**
   - Cada classe de teste de integração (ou fluxo completo de teste) deve possuir e rodar em seu próprio banco de dados e contexto isolados, garantindo que não haja poluição de dados entre as execuções de testes.
3. **Resiliência:**
   - Garanta que as configurações de conexão dos containers tenham políticas de retry automáticas para tolerar latência na inicialização dos containers.
4. **Validação do Fluxo Real:**
   - Teste fluxos ponta a ponta (como criar chamado, tramitar, persistir e buscar no banco de dados, gravar no Redis) para validar a integridade de dados e a camada de infraestrutura.
