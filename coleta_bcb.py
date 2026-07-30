import requests
import pandas as pd
from datetime import datetime, timedelta

def coletar_selic():
    print("Iniciando coleta de dados do Banco Central...")

    data_final = datetime.today().strftime('%d/%m/%Y')
    data_inicial = (datetime.today() - timedelta(days=365*5)).strftime('%d/%m/%Y')  # últimos 5 anos

    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"
        f"?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        dados_json = response.json()
        print(f"Sucesso! {len(dados_json)} registros encontrados.")

        df = pd.DataFrame(dados_json)
        print(df.head())

        df.to_csv("selic.csv", index=False, sep=';')
        print("Arquivo 'selic.csv' criado com sucesso.")

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API: {e}")

if __name__ == "__main__":
    coletar_selic()