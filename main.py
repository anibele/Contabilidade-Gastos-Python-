import pandas as pd
import sys

def analisar_e_classificar(descricao):
    """
    O 'cérebro' do algoritmo. Ele lê a descrição do gasto e
    retorna a classificação contábil correta com base em palavras-chave.
    """
    texto = str(descricao).lower()
    
    if "programador" in texto:
        return "Custo Fixo"
    elif "comissão" in texto or "comissao" in texto:
        return "Despesa Variável"
    elif "estagiário" in texto or "estagiario" in texto:
        return "Despesa Fixa"
    elif "licenças" in texto or "licencas" in texto or "software" in texto:
        return "Custo Variável"
    elif "imposto" in texto or "iss" in texto:
        return "Despesa Variável"
    elif "pró-labore" in texto or "pro-labore" in texto or "lucas" in texto:
        return "Despesa Fixa"
    elif "internet" in texto:
        return "Custo Fixo"
    elif "material" in texto or "limpeza" in texto:
        return "Despesa Fixa"
    else:
        return "Não Classificado"

def carregar_dados(caminho="Dados - Empresa Giga.xlsx"):
    """
    Lê a planilha Excel, extrai as descrições e os valores, e pede para
    o algoritmo classificar conta por conta automaticamente.
    """
    try:
        # Lê o Excel. O header=0 garante que ele pule o cabeçalho original
        df = pd.read_excel(caminho, header=0)
        
        # Vamos pegar as colunas pelo índice para evitar erros de nome de coluna
        # Assumimos que a Coluna 2 (índice 1) é a Descrição e a Coluna 3 (índice 2) é o Valor.
        descricao_col = df.columns[1]
        valor_col = df.columns[2]
        
        # Criamos um DataFrame limpo apenas com o que importa
        df_limpo = pd.DataFrame()
        df_limpo["descricao"] = df[descricao_col]
        df_limpo["valor"] = df[valor_col]
        
        df_limpo["valor"] = df_limpo["valor"].astype(str)
        df_limpo["valor"] = df_limpo["valor"].str.replace("R$", "", regex=False).str.replace(" por unidade", "", regex=False).str.strip()
        df_limpo["valor"] = df_limpo["valor"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
        df_limpo["valor"] = pd.to_numeric(df_limpo["valor"], errors="coerce").fillna(0)
        
       
        # Aplica a nossa função de análise linha por linha
        df_limpo["classificacao"] = df_limpo["descricao"].apply(analisar_e_classificar)
            
        return df_limpo.to_dict(orient="records")
        
    except FileNotFoundError:
        print("\n[Aviso] Arquivo Excel não encontrado.")
        print("Carregando o banco de dados interno da 'Atividade Gustavo Anibele'...\n")
        return [
            {"descricao": "Salário da equipe de programadores", "valor": 6000.00, "classificacao": "Custo Fixo"},
            {"descricao": "Comissão de 5% sobre o valor do serviço", "valor": 750.00, "classificacao": "Despesa Variável"},
            {"descricao": "Estagiário para o administrativo", "valor": 1200.00, "classificacao": "Despesa Fixa"},
            {"descricao": "Licenças de software de desenvolvimento", "valor": 800.00, "classificacao": "Custo Variável"},
            {"descricao": "Imposto sobre Serviços (ISS) de 5%", "valor": 750.00, "classificacao": "Despesa Variável"},
            {"descricao": "Pró-labore do Lucas (Sócio-Administrador)", "valor": 3000.00, "classificacao": "Despesa Fixa"},
            {"descricao": "Conta de internet dedicada da empresa", "valor": 250.00, "classificacao": "Custo Fixo"},
            {"descricao": "Material de escritório e limpeza", "valor": 150.00, "classificacao": "Despesa Fixa"}
        ]

def classificar_operacionalmente(contas):
    """
    Agrupa as contas puramente pelo seu comportamento: Fixos x Variáveis.
    """
    balanco = {
        "variaveis": [], 
        "fixos": []      
    }

    for conta in contas:
        classificacao = str(conta["classificacao"]).lower()

        if "variável" in classificacao or "variavel" in classificacao:
            balanco['variaveis'].append(conta)
        elif "fixo" in classificacao or "fixa" in classificacao:
            balanco['fixos'].append(conta)

    return balanco

def exibir_relatorio_contabil(dados_brutos, balanco):
    """
    Calcula os indicadores contábeis e imprime o relatório.
    """
    faturamento = 15000.00
    
    total_variaveis = sum(item["valor"] for item in balanco['variaveis'])
    total_fixos = sum(item["valor"] for item in balanco['fixos'])
    
    if total_variaveis == 0 and total_fixos == 0:
        print("\n[Erro Crítico] Nenhuma conta classificada. Verifique o arquivo Excel.")
        return

    mc_valor = faturamento - total_variaveis
    mc_percentual = mc_valor / faturamento
    ponto_equilibrio = total_fixos / mc_percentual

    print("-" * 60)
    print("RELATÓRIO CONTÁBIL - ATIVIDADE".center(60))
    print("-" * 60)

    print("\n[ Questão 1 - Classificação Inicial (Custo vs. Despesa) ]")
    print("Resposta: Os gastos foram classificados automaticamente da seguinte forma:")
    for i, item in enumerate(dados_brutos, start=1):
        print(f" {i}. {item['descricao']} | R$ {item['valor']:.2f} | {item['classificacao']}")

    print("\n")
    print("\n[ Questão 2 - Classificação Operacional (Fixo vs. Variável) ]")
    
    print("\n2.1. O que varia diretamente de acordo com o volume de serviços ou faturamento (Variável)?")
    print(f"Resposta: Comissão para o vendedor, licenças de software e imposto sobre serviços.")
    
    print("\n2.2. O que se mantém estavel independentemente do volume (Fixo)?")
    print(f"Resposta: Salário dos programadores, salário do estagiário, pró-labore do Lucas, conta de internet dedicada e material de escritório e limpeza.")

    print("\n")
    print("\n[ Questão 3 - Cálculo da Margem de Contribuição e Ponto de Equilíbrio ]")
    
    print(f"Total de Gastos Variáveis: R$ {total_variaveis:,.2f} (Comissão R$ 750 + Licenças R$ 800 + ISS R$ 750)")
    print(f"Total de Gastos Fixos: R$ {total_fixos:,.2f} (Programadores R$ 6000 + Estagiário R$ 1200 + Pró-labore R$ 3000 + Internet R$ 250 + Limpeza R$ 150)")

    print("\n3.1. Margem de Contribuição Total (R$) e Percentual (%)")
    print(f"Resposta: Margem de Contribuição Total = 15.000,00 - {total_variaveis:,.2f} = R$ {mc_valor:,.2f}")
    print(f"Resposta: Margem de Contribuição % = ({mc_valor:,.2f} / 15.000,00) * 100 = {mc_percentual*100:.2f}%")

    print("\n3.2. O Ponto de Equilíbrio Financeiro/Operacional (R$) necessário para a empresa não ter prejuízo.")
    print(f"Resposta: Ponto de Equilíbrio = {total_fixos:,.2f} / {mc_percentual:.4f} = R$ {ponto_equilibrio:,.2f}")

    print("\n3.3. Análise Crítica: O valor de R$ 15.000,00 cobrado pelo programador é vantajoso?")
    print("Resposta: Sim, pois a empresa consegue gerar lucro líquido com esse valor, apesar de ser um valor baixo.")
    print("\n")


def menu():
    """
    Menu principal da aplicação.
    """
    dados_brutos = carregar_dados()
    balanco_operacional = classificar_operacionalmente(dados_brutos)

    while True:
        print("\n")
        print("       MENU PRINCIPAL       ")
        print("1 - Mostrar Resultados da Atividade")
        print("2 - Sair do Sistema")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            exibir_relatorio_contabil(dados_brutos, balanco_operacional)
        elif opcao == '2':
            print("\nEncerrando o sistema.")
            sys.exit()
        else:
            print("\n[Erro] Opção inválida. Digite 1 ou 2.\n")


if __name__ == "__main__":
    menu()