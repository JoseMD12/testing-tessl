# Agent Rules <!-- tessl-managed -->

@.tessl/RULES.md follow the [instructions](.tessl/RULES.md)

## Diretrizes do Projeto (AI-Native & SDD - .NET 8)

Este projeto segue uma abordagem AI-Native combinada com SDD (Schema/Spec Driven Development) usando .NET 8.

---

### 🧭 Roteamento de Instruções para Agentes de IA

Para manter o contexto enxuto e livre de redundâncias, as diretrizes de desenvolvimento deste repositório foram modularizadas:

1. **Aprovação de Terminal e Comandos:** As restrições de execução e segurança estão descritas na regra do Tessl em [terminal-approval-flow.md](file:///mnt/c/Users/jose.dotta/Documents/Projects/SDD-Usage/MachineReturnProto/plugins/dotnet-clean-arch/rules/terminal-approval-flow.md).
2. **Formato e Criação de Specs (SDD):** As diretrizes de nomenclatura e templates obrigatórios de especificação estão delegadas à skill do Tessl [SKILL.md](file:///mnt/c/Users/jose.dotta/Documents/Projects/SDD-Usage/MachineReturnProto/plugins/dotnet-clean-arch/skills/sdd-spec-enforcer/SKILL.md).
3. **Outras Habilidades Técnicas:** Habilidades específicas para gerar testes unitários (xUnit/Moq), testes de integração (Testcontainers) e fatias verticais estão configuradas nos plugins locais do Tessl (verifique [tessl.json](file:///mnt/c/Users/jose.dotta/Documents/Projects/SDD-Usage/MachineReturnProto/tessl.json)).

Antes de codificar qualquer nova funcionalidade, localize e leia a especificação correspondente (`spec-*.md`) no diretório `/specs` ou `/docs/specs`.

---

### 🏢 Tema de Domínio: MachineReturn (Logística Reversa de Máquinas Corporativas)
Sistema de gerenciamento de devolução de máquinas corporativas por fim de contrato ou defeito, integrando triagem automática de destino e inspeção de qualidade de hardware.

#### Fluxo de Negócio e Personas:
1. **Abertura de Chamado (Consumidor - Sem Login):** 
   - Um consumidor abre um chamado de devolução informando apenas o **código da máquina** e o **e-mail** associado a ela.
   - O sistema valida se o e-mail corresponde ao usuário atualmente atribuído à máquina.
   - A devolução é motivada por: **Tempo de Aluguel Expirado** ou **Produto com Erro**.
2. **Triagem Automática de Fábrica:**
   - Com base no ano de fabricação, origem da máquina e número de série, o sistema calcula para qual **Fábrica Cadastrada** a máquina deve ser enviada fisicamente.
3. **Inspeção de Qualidade (Agente de Qualidade - Com Login):**
   - Na fábrica receptora, um Agente de Qualidade realiza a averiguação física.
   - Ele define o **Selo de Qualidade** da máquina: `Novo`, `UsadoEmBoasCondicoes`, `Usado`, `NecessitaManutencao`, `Desmontar`, `Descartar`.
   - Com base no selo e nas regras, o agente decide o destino operacional da máquina.

#### Entidades do Domínio (Classes Ricas):
- **Usuario e Perfil:** Perfis como `Consumidor` (sem acesso de login ao sistema) e `AgenteQualidade` (com login).
- **Maquina:** Código único, número de série, ano de fabricação, país de origem, usuário atribuído atual e histórico de selos de qualidade.
- **ChamadoDevolucao:** Ciclo de vida (`Aberto`, `EmTransito`, `Recebido`, `Inspecionado`, `Finalizado`), motivo do chamado, fábrica de destino e histórico de tramitação.
- **Fabrica:** Nome, país e capacidade operacional.
- **LaudoQualidade:** Resultado da averiguação do Agente de Qualidade contendo o selo atribuído e o parecer técnico.

#### Regra de Roteamento (Exemplo):
- **Fábrica de Destino:**
  - Máquinas com **origem** fora das Américas e **ano de fabricação** menor que 2021 são direcionadas para a Fábrica de Descarte Internacional.
  - Máquinas com **motivo** "Produto com Erro" e **número de série** iniciado com "CN" vão para a Fábrica de Manutenção Avançada.

---

### 🏛️ Arquitetura do Sistema
O projeto é dividido em módulos estruturados combinando conceitos de **Clean Architecture** e **Vertical Slice Architecture**:

1. **Domain:**
   - Contém a lógica central de negócio (Entidades, Agregados, Objetos de Valor) e regras corporativas.
   - **Regra:** Seguir os padrões do **Domain-Driven Design (DDD)** e **Classes Ricas** (encapsulamento de comportamento de mudança de estado e validações):
     - **Aggregate Roots:** Ponto de entrada do agregado que garante a consistência das invariantes (ex: `ChamadoDevolucao` controlando a tramitação).
     - **Entities:** Objetos com identidade única que persiste ao longo do tempo (ex: `Maquina`, `Usuario`, `Fabrica`).
     - **Value Objects:** Objetos imutáveis definidos pelos seus atributos e sem identidade própria (ex: `SeloQualidade`, `SerialNumber`, `EmailAddress`).
     - Evitar modelos anêmicos (apenas com get/set públicos) para facilitar a testabilidade.
2. **Application:**
   - Orquestra os casos de uso da aplicação.
   - **Regra:** Dividido por **Vertical Slices** (Features). Cada feature encapsula seu request, handler, lógica de validação específica e resposta no mesmo escopo/módulo.
3. **Infra:**
   - Implementação de acesso a dados (PostgreSQL via Entity Framework Core ou Dapper), persistência e infraestrutura de Cache (Redis).
   - Integrações externas e configurações de infraestrutura.
4. **API:**
   - Ponto de entrada da aplicação (.NET 8 Minimal APIs ou Controllers).
   - Mapeamento de rotas e contratos de Request/Response expostos.
5. **Shared:**
   - Tratamento global de erros (Error/Exception Handling Middleware).
   - **Regra:** Deve conter o middleware global de exceção que captura exceções de domínio/negócio (ex: `DomainException`) e as mapeia para respostas HTTP semânticas (ex: `400 Bad Request`, `422 Unprocessable Entity`), evitando blocos try-catch manuais na camada de API.
   - Respostas de erro padronizadas e classes utilitárias compartilhadas entre os projetos.

---

### 💾 Banco de Dados, Cache e Configurações
- **Escrita:** PostgreSQL.
- **Cache:** Redis.
- **Orquestração local:** O projeto deve conter um `docker-compose.yml` e arquivos `Dockerfile` configurados para subir a aplicação e suas dependências locais de forma rápida.
- **Dados Iniciais (Seeds):** Deve existir uma carga inicial (seed) automática de banco para cadastrar um Usuário Administrador padrão (`admin`) com o perfil de administrador correspondente.
- **Configurações e Segredos:** Todas as credenciais de banco, portas de Redis e dados sensíveis de seed devem ser lidas a partir de variáveis de ambiente no Docker/Produção e utilizando **User Secrets** do .NET (`dotnet user-secrets`) durante o desenvolvimento local. Nunca expor segredos no repositório.
- **EF Core Migrations:** A geração de migrações e o contexto do banco de dados devem residir na camada `Infra`. As migrações pendentes devem ser aplicadas automaticamente na inicialização da aplicação em ambiente de desenvolvimento local.
- **Resiliência e Políticas de Retry:** Configurar políticas de resiliência e tentativas de conexão (como `EnableRetryOnFailure` do EF Core para o PostgreSQL) para evitar falhas na inicialização caso a aplicação suba enquanto os containers de banco de dados ou Redis ainda estejam iniciando.

---

### 🧪 Estratégia de Testes
Toda feature desenvolvida deve ser acompanhada de:
1. **Testes Unitários:** Focados em testar isoladamente as regras de negócio expostas no Domain e Application.
   - **Regra:** Cada seção de domínio ou Aggregate Root deve ter seus próprios arquivos de testes unitários dedicados.
   - **Isolamento e Mocks:** Devem ser totalmente isolados de dependências externas. Utilizar frameworks de Mock (como NSubstitute ou Moq) para simular comportamentos de repositórios, serviços e componentes externos.
2. **Testes de Integração:** Devem testar o fluxo de ponta a ponta.
   - **Regra:** Utilizar **Testcontainers** para criar instâncias reais e efêmeras de PostgreSQL e Redis durante a execução dos testes de integração, garantindo isolamento e fidelidade aos ambientes reais.
   - **Isolamento de Banco:** Cada classe de teste ou execução de fluxo de integração deve possuir e rodar em seu próprio banco de dados e contexto isolados, garantindo que não haja poluição de estado entre os testes executados.

---

### 📞 Testes Manuais (Arquivos `.http`)
- Para facilitar testes rápidos da API sem a necessidade de ferramentas externas (como Postman), arquivos com extensão `.http` devem ser criados na camada de API ou em uma pasta dedicada `/requests` na raiz do projeto.
- **Regra:** Cada seção de domínio ou Aggregate Root deve ter seu próprio arquivo `.http` individual (ex: `requests/machine-returns.http`) para manter os testes manuais focados por contexto.

---

### 📦 Padrões de Arquivos e Git
- **.gitignore:** Deve ser mantido limpo e atualizado com as pastas geradas pelo ecossistema do .NET (`bin/`, `obj/`, `.vs/`, `.idea/`, arquivos `.user`, segredos locais de desenvolvimento e configurações sensíveis).
