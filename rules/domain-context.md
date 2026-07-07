# Tema de Domínio: MachineReturn (Logística Reversa de Máquinas Corporativas)

Este documento descreve as regras de negócio, personas, fluxo operacional e entidades da aplicação MachineReturn.

---

## 🔄 Fluxo de Negócio e Personas

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

---

## 🏢 Entidades do Domínio (Classes Ricas)

- **Usuario e Perfil:** Perfis como `Consumidor` (sem acesso de login ao sistema) e `AgenteQualidade` (com login).
- **Maquina:** Código único, número de série, ano de fabricação, país de origem, usuário atribuído atual e histórico de selos de qualidade.
- **ChamadoDevolucao:** Ciclo de vida (`Aberto`, `EmTransito`, `Recebido`, `Inspecionado`, `Finalizado`), motivo do chamado, fábrica de destino e histórico de tramitação.
- **Fabrica:** Nome, país e capacidade operacional.
- **LaudoQualidade:** Resultado da averiguação do Agente de Qualidade contendo o selo atribuído e o parecer técnico.

---

## 🚦 Regra de Roteamento (Exemplo)

- **Fábrica de Destino:**
  - Máquinas com **origem** fora das Américas e **ano de fabricação** menor que 2021 são direcionadas para a Fábrica de Descarte Internacional.
  - Máquinas com **motivo** "Produto com Erro" e **número de série** iniciado com "CN" vão para a Fábrica de Manutenção Avançada.
