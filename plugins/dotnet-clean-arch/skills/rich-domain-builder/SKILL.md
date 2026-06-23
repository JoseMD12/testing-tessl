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
   - Controle a consistência e integridade das invariantes de todo o grupo de entidades sob sua raiz.
   - Exemplo: Uma raiz de agregado controla as mudanças de estado e as regras de transição de ciclo de vida de suas entidades internas, garantindo que o objeto nunca entre em estado inválido.
3. **Entities (Entidades):**
   - Objetos com uma identidade única e contínua ao longo do tempo (possuem ID de entidade).
4. **Value Objects (Objetos de Valor):**
   - Objetos imutáveis definidos unicamente por seus atributos, sem identidade própria.
   - Devem estender uma classe base `ValueObject` comum que implementa a igualdade estrutural.
5. **Validações de Domínio:**
   - Execute as validações de consistência e invariantes diretamente nas entidades e Value Objects.
   - Lance uma exceção de domínio (ex: `DomainException`) caso alguma regra descrita na especificação correspondente seja violada.
6. **Fonte de Regras de Negócio (SDD):**
   - As regras de negócio específicas (como condições de transição, limites e cálculos) devem ser extraídas exclusivamente dos arquivos de especificação (`spec-*.md`). Não defina ou infira regras de negócio com base em diretrizes desta skill.
