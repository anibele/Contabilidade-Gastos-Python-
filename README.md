# Sistema Automático de Contabilidade Gerencial - Caso Giga

Este repositório contém uma solução em Python desenvolvida para automatizar a classificação de gastos e o cálculo de indicadores de Contabilidade Gerencial. O algoritmo atua como um analista financeiro, lendo dados brutos, interpretando textos para classificar despesas/custos e gerando um relatório estruturado para apoio à tomada de decisão.

---

## Contexto da Atividade

A **Giga** é uma microempresa especializada no desenvolvimento e suporte de softwares de automação comercial para pequenas lojas. Recentemente, a empresa fechou um contrato recorrente para prestar serviços de Suporte Técnico e Manutenção de Sistemas para um grande cliente.

O programador sênior e fundador da empresa, Lucas, deparou-se com um dilema: ele fechou esse contrato cobrando um valor fixo de **R$ 15.000,00 por mês**, mas tem a incerteza se esse valor realmente cobre os gastos da estrutura e gera o lucro esperado. 

Para ajudá-lo, desenvolvemos este algoritmo que processa o relatório financeiro do último mês (com todos os desembolsos vinculados à operação do serviço) e calcula se a precificação de Lucas foi, de fato, vantajosa.

---

## Conceitos Contábeis Aplicados

Para auxiliar o Lucas, o sistema não separa puramente os valores em "Custos" e "Despesas". Na Contabilidade Gerencial, para calcular o Ponto de Equilíbrio, focamos no **comportamento** dos gastos em relação ao faturamento:

* **Gastos Fixos:** Valores que a Giga precisará pagar independentemente de quantos serviços prestar (ex: Salários, Pró-labore, Internet).
* **Gastos Variáveis:** Valores que aumentam ou diminuem de acordo com o faturamento ou volume de serviços (ex: Impostos, Comissões, Licenças por usuário ativo).

A partir dessa separação, o algoritmo calcula três indicadores vitais:

**1. Margem de Contribuição (MC):**
Representa o quanto sobra da receita do contrato após o pagamento de todos os gastos variáveis. É o valor que "contribui" para pagar os gastos fixos e gerar lucro.
$$MC = Faturamento - Gastos\ Variáveis$$

**2. Índice de Margem de Contribuição (IMC):**
É a representação percentual da Margem de Contribuição sobre o faturamento.
$$IMC = \frac{MC}{Faturamento}$$

**3. Ponto de Equilíbrio Operacional (PE):**
Indica o faturamento exato (em R$) que a empresa precisa alcançar para pagar todos os seus gastos (zero lucro, zero prejuízo).
$$PE = \frac{Gastos\ Fixos}{IMC}$$

---

## Arquitetura e Funções do Código

O script principal foi construído com foco em resiliência e automação. Abaixo, as principais funções do algoritmo:

* `analisar_e_classificar(descricao)`: Atua como o "cérebro" do sistema. É um classificador baseado em palavras-chave (NLP simples) que lê a descrição do gasto no arquivo bruto e deduz automaticamente se é um Custo Fixo, Custo Variável, Despesa Fixa ou Despesa Variável, sem precisar que a planilha tenha essa informação previamente anotada.
* `carregar_dados(caminho)`: Responsável por ler o arquivo `.xlsx` ou `.csv` usando a biblioteca Pandas. Possui uma camada de segurança (fallback) que injeta o banco de dados padrão do caso Giga na memória caso o arquivo externo não seja encontrado. Limpa e converte strings financeiras (ex: "R$ 6.000,00") para formato numérico tratável no Python.
* `classificar_operacionalmente(contas)`: Agrupa as contas previamente analisadas em dois grandes blocos estritos: **Fixos** e **Variáveis**, preparando-os para os cálculos gerenciais.
* `exibir_relatorio_contabil(dados_brutos, balanco)`: Executa as fórmulas matemáticas contábeis e formata a saída de dados no terminal de forma clara, amigável e fidedigna às exigências acadêmicas/profissionais.
* `menu()`: Interface de usuário baseada em terminal (CLI) que permite navegar entre visualizar o relatório ou sair do programa.

---

## Resultados Obtidos

Após o processamento dos dados da Giga, o algoritmo apresentou o seguinte cenário financeiro para o contrato de **R$ 15.000,00**:

* **Total de Gastos Variáveis:** R$ 2.300,00
* **Total de Gastos Fixos:** R$ 10.600,00
* **Margem de Contribuição:** R$ 12.700,00 (que representa **84,67%** de IMC).
* **Ponto de Equilíbrio:** R$ 12.519,69.

**Análise Crítica:** O algoritmo provou que o valor de R$ 15.000,00 cobrado por Lucas é **vantajoso**. O faturamento supera o Ponto de Equilíbrio (R$ 12.519,69), o que significa que a estrutura se paga e a operação do serviço consegue gerar lucro líquido positivo para a Giga, apesar de a precificação poder ser considerada baixa para os padrões do mercado.

As respostas também podem ser vistas no pdf: 
[Resultados.pdf](./Resultados.pdf)

---

### Pré-requisitos
* **Python 3.8+** instalado em sua máquina.
* Bibliotecas do Python: `pandas` e `openpyxl`.
