---
name: rich-domain-builder
description: Ativado ao definir ou modificar Aggregate Roots, Entities ou Value Objects na camada de domínio, garantindo o encapsulamento correto e evitando modelos anêmicos.
---

# Rich Domain Builder

Esta habilidade orienta a definição, escrita e validação de entidades de domínio ricas no padrão DDD (Domain-Driven Design), garantindo encapsulamento correto e evitando modelos anêmicos.

## Diretrizes do Domínio

1. **Modelos Ricos (Rich Domain Models):**
   - Evite classes anêmicas compostas apenas por propriedades com getters e setters públicos automáticos (`{ get; set; }`).
   - Propriedades devem ter setters privados ou protegidos (`{ get; private set; }`).
   - Mudanças de estado devem ocorrer exclusivamente por meio de métodos de negócios explícitos (ex: `AlterarStatus(Status status)`, `RegistrarLaudo(...)`).
2. **Aggregate Roots (Raízes de Agregado):**
   - Controle a consistência e integridade das invariantes do grupo de entidades.
   - Exemplo: `ChamadoDevolucao` gerencia as transições de status (`Aberto` -> `EmTransito` -> `Recebido` -> `Inspecionado` -> `Finalizado`) e o cálculo da fábrica de destino.
3. **Entities (Entidades):**
   - Objetos com uma identidade única persistente. Exemplo: `Maquina`, `Usuario`, `Fabrica`.
4. **Value Objects (Objetos de Valor):**
   - Objetos imutáveis definidos por seus atributos, sem identidade própria (ex: `SeloQualidade`, `SerialNumber`, `EmailAddress`).
   - Devem estender uma classe base `ValueObject` comum que implementa a igualdade estrutural.
5. **Validações e Exceções de Domínio:**
   - Valide as regras de negócio nas próprias entidades e Value Objects.
   - Lance `DomainException` quando uma regra de negócio for violada.
