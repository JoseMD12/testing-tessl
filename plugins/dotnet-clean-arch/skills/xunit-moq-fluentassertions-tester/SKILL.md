---
name: xunit-moq-fluentassertions-tester
description: Ativado ao gerar testes de unidade para entidades do Domain ou handlers da Application usando a stack xUnit + Moq + FluentAssertions.
---

# Unit Testing with xUnit, Moq, and FluentAssertions

Esta habilidade orienta a criação de testes unitários rápidos, isolados e focados nas regras de negócios expostas no Domain e Application.

## Diretrizes de Testes Unitários

1. **Estrutura e Nomenclatura:**
   - Use o padrão AAA (Arrange, Act, Assert).
   - Nomeie os métodos de teste de forma semântica, descrevendo o comportamento esperado: `Deve_LancarExcecao_Quando_ChamadoJaFinalizado` ou `Should_TransitionToEmTransito_When_ShipmentDispatched`.
2. **Mocks e Isolamento:**
   - Use Moq (ou NSubstitute se configurado) para mockar repositórios, serviços externos e dependências de infraestrutura.
   - Testes unitários do Domain/Application não devem acessar bancos de dados reais, cache, sistemas de arquivos ou APIs de terceiros.
3. **Asserções:**
   - Utilize a biblioteca FluentAssertions para criar asserções legíveis (ex: `result.Should().BeTrue()`, `act.Should().Throw<DomainException>()`).
4. **Foco Contextual:**
   - Crie um arquivo de testes unitários para cada Aggregate Root ou Feature do Application.
