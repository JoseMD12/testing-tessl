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

1. **Payload de Entrada do Chamado (`POST /api/v1/return-requests`):**
   * Deve aceitar os seguintes campos obrigatórios:
     * `machineCode` (string)
     * `email` (string, formato válido)
     * `city` (string)
     * `reasonCode` (enum: `TempoDeAluguelExpirado`, `ProdutoComErro`)
     * `needsCollection` (boolean)
   * Deve aceitar campos opcionais:
     * `description` (string, até 500 caracteres, opcional)
     * `collectionAddress` (objeto contendo `street`, `number`, `city`, `state`, `zipCode`; obrigatório se `needsCollection` for `true`, nulo caso contrário)

2. **Validações de Domínio:**
   * **Validação de Vínculo de Máquina:** O sistema deve consultar uma base cadastral externa simulada para verificar se o `email` informado corresponde ao usuário (CPF) atualmente atribuído ao `machineCode`. Caso não haja correspondência, deve retornar erro semântico de domínio (`422 Unprocessable Entity` ou `400 Bad Request`).
   * **Validação de Chamado Ativo:** Uma máquina só pode possuir um único chamado de devolução ativo (Status diferente de `Finalizado`). Se já houver um chamado em andamento, deve impedir a criação retornando erro de duplicidade (`400 Bad Request`).
   * Um mesmo usuário (portador) pode possuir múltiplos chamados ativos desde que sejam para máquinas distintas.

3. **Status Inicial e Criação:**
   * O endpoint de abertura deve responder com status `201 Created` e um objeto contendo apenas `id` (Guid), `status` (string) e `city` (string).
   * O status inicial do chamado será:
     * `AguardandoAgendamentoColeta` se `needsCollection` for `true`.
     * `Criado` se `needsCollection` for `false`.

4. **Triagem de Fábrica Assíncrona:**
   * Ao criar o chamado, deve ser disparado o evento de domínio `ReturnRequestOpenedDomainEvent`.
   * Um handler de evento de domínio assíncrono será responsável por disparar a regra de triagem automática e associar a fábrica de destino ao chamado.

5. **Associação de Ponto de Entrega (`PATCH /api/v1/return-requests/{id}/delivery-point`):**
   * Caso `needsCollection` seja `false` e o chamado esteja com status `Criado`, o usuário poderá associar um ponto de entrega físico através deste endpoint.
   * O payload deve conter `deliveryPointId` (Guid, obrigatório).
   * Após a associação bem-sucedida, o status do chamado deve transitar para `AguardandoEntrega`.
   * Se o chamado já possuir coleta (`needsCollection == true`) ou não estiver no status `Criado`, o endpoint deve retornar erro de validação.

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
