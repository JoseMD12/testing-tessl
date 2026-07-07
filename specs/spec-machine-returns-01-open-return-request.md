---
id: SR-01-OPEN-RETURN-REQUEST
feature: OpenReturnRequest
pod: MachineReturns
priority: High
iteration: Iteration 1
contract: OpenAPI / Swagger (Minimal APIs .NET 8)
---

# Abertura de Chamado de Devolução (OpenReturnRequest)

## User Value

Como portador atual de uma máquina alugada (notebook corporativo), desejo abrir um chamado de devolução sem necessidade de realizar login, fornecendo apenas o código da máquina, e-mail associado e dados de logística. Isso me permite dar início ao processo de logística reversa e escolher se entregarei em um ponto físico ou se solicitarei coleta em meu endereço.

## Acceptance Criteria

### Cenário 1: Payload de entrada inválido ao abrir chamado (Campos obrigatórios ausentes ou incorretos)

Dado que um consumidor tenta abrir um chamado de devolução enviando um payload incompleto ou incorreto
Quando a requisição `POST /api/v1/return-requests` é processada
Então o sistema deve retornar erro de validação (HTTP 400 Bad Request) detalhando quais campos estão inválidos ou ausentes.

*Campos obrigatórios: `machineCode` (string), `email` (string, formato válido), `city` (string), `reasonCode` (enum: `TempoDeAluguelExpirado`, `ProdutoComErro`), `needsCollection` (boolean).*
*Campos opcionais: `description` (string, até 500 caracteres), `collectionAddress` (objeto contendo `street`, `number`, `city`, `state`, `zipCode`; obrigatório se `needsCollection` for `true`, nulo caso contrário).*

### Cenário 2: Validação de vínculo de máquina inválido (E-mail não correspondente)

Dado que um consumidor tenta abrir um chamado para a máquina com código "MAC-998877" informando o e-mail "<outro@empresa.com>"
E a base cadastral de ativos corporativos indica que a máquina está atribuída a "<colaborador@empresa.com>"
Quando a requisição `POST /api/v1/return-requests` é processada
Então o sistema deve retornar um erro semântico de domínio (HTTP 400 Bad Request ou 422 Unprocessable Entity) indicando a falta de vínculo.

### Cenário 3: Validação de chamado ativo em andamento (Duplicidade)

Dado que a máquina "MAC-998877" já possui um chamado de devolução ativo (com status diferente de "Finalizado")
Quando o consumidor tenta abrir um novo chamado para a mesma máquina com a requisição `POST /api/v1/return-requests`
Então o sistema deve recusar a criação e retornar erro de duplicidade (HTTP 400 Bad Request).
*Nota: Um mesmo usuário (portador) pode possuir múltiplos chamados ativos desde que sejam para máquinas distintas.*

### Cenário 4: Abertura de chamado válida com solicitação de coleta (needsCollection = true)

Dado que o consumidor informa um código de máquina "MAC-998877" e e-mail "<colaborador@empresa.com>" correspondentes na base cadastral
E a máquina não possui chamados ativos
E o campo `needsCollection` é definido como `true` com um `collectionAddress` válido
Quando a requisição `POST /api/v1/return-requests` é processada
Então o sistema deve retornar status HTTP 201 Created contendo o `id` (Guid), o status inicial "AguardandoAgendamentoColeta" e a `city` correspondente
E deve disparar o evento de domínio `ReturnRequestOpenedDomainEvent` assincronamente para realizar a triagem de fábrica.

### Cenário 5: Abertura de chamado válida para entrega em ponto físico (needsCollection = false)

Dado que o consumidor informa um código de máquina "MAC-998877" e e-mail "<colaborador@empresa.com>" correspondentes na base cadastral
E a máquina não possui chamados ativos
E o campo `needsCollection` é definido como `false`
Quando a requisição `POST /api/v1/return-requests` é processada
Então o sistema deve retornar status HTTP 201 Created contendo o `id` (Guid), o status inicial "Criado" e a `city` correspondente
E deve disparar o evento de domínio `ReturnRequestOpenedDomainEvent` assincronamente para realizar a triagem de fábrica.

### Cenário 6: Associação bem-sucedida de ponto de entrega físico

Dado um chamado de devolução existente com ID "7690bc4d-5872-4638-b7a4-e91b689cf912", status igual a "Criado" (needsCollection = false) e sem ponto de entrega associado
Quando o consumidor envia uma requisição `PATCH /api/v1/return-requests/7690bc4d-5872-4638-b7a4-e91b689cf912/delivery-point` com o `deliveryPointId` (Guid)
Então o sistema deve associar o ponto de entrega ao chamado, transitar seu status para "AguardandoEntrega" e responder com status HTTP 204 No Content.

### Cenário 7: Falha ao associar ponto de entrega a chamado incompatível

Dado um chamado de devolução existente com ID "7690bc4d-5872-4638-b7a4-e91b689cf912" que foi criado com needsCollection = true (status "AguardandoAgendamentoColeta")
Quando o consumidor tenta associar um ponto de entrega físico enviando `PATCH /api/v1/return-requests/7690bc4d-5872-4638-b7a4-e91b689cf912/delivery-point`
Então o sistema deve rejeitar a solicitação e retornar erro de validação (HTTP 400 Bad Request).

## Data Model

### Entidade `ChamadoDevolucao` (Aggregate Root)

* `Id` (Guid, Chave Primária)
* `MachineCode` (string, indexado)
* `RequesterEmail` (string)
* `City` (string)
* `Reason` (Enum: `TempoDeAluguelExpirado`, `ProdutoComErro`)
* `Description` (string, opcional, nulo se não fornecido)
* `NeedsCollection` (boolean)
* `CollectionAddress` (Value Object contendo `Street`, `Number`, `City`, `State`, `ZipCode` - opcional, nulo se `NeedsCollection` for falso)
* `DeliveryPointId` (Guid, opcional, nulo se não definido)
* `Status` (Enum: `Criado`, `AguardandoAgendamentoColeta`, `AguardandoEntrega`, `EmTransito`, `Recebido`, `Inspecionado`, `Finalizado`)
* `AssignedFactoryId` (Guid, opcional, nulo até que a triagem ocorra)
* `CreatedAt` (DateTime)

## Security Constraints

* Endpoint público (sem necessidade de login ou token JWT).
* Sanitização obrigatória dos campos de texto (`description` e `collectionAddress.street`) contra injeções.
* Proteção contra DDoS e força bruta no envio de solicitações utilizando o mesmo e-mail ou código de máquina em janelas curtas de tempo.

## API Contract

### `POST /api/v1/return-requests`

**Request Body:**

```json
{
  "machineCode": "MAC-998877",
  "email": "colaborador@empresa.com",
  "city": "São Paulo",
  "reasonCode": "ProdutoComErro",
  "description": "Tela piscando sem parar",
  "needsCollection": true,
  "collectionAddress": {
    "street": "Avenida Paulista",
    "number": "1000",
    "city": "São Paulo",
    "state": "SP",
    "zipCode": "01310-100"
  }
}
```

**Response (201 Created):**

```json
{
  "id": "7690bc4d-5872-4638-b7a4-e91b689cf912",
  "status": "AguardandoAgendamentoColeta",
  "city": "São Paulo"
}
```

### `PATCH /api/v1/return-requests/{id}/delivery-point`

**Request Body:**

```json
{
  "deliveryPointId": "a90184bc-de4f-4d92-bf39-4d6d67b21234"
}
```

**Response (204 No Content):**
*(Sem corpo de resposta)*

## Dependencies

* Serviço de validação de portador (integração fictícia com banco/base cadastral de ativos corporativos).
* Sistema de consulta de Pontos de Entrega disponíveis por cidade (para o frontend/consumidor escolher onde entregar).
* Event Broker ou mecanismo de mensageria em memória (como o `MediatR` no .NET 8) para processar a triagem de fábrica de forma assíncrona.

## Out of Scope

* O algoritmo detalhado da **Triagem de Fábrica** (será mapeado em outra especificação de negócio dedicada).
* Cadastro e administração de Pontos de Entrega.
* Autenticação via login para o consumidor (apenas validação cadastral).
