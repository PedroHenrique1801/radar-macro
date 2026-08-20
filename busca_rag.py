import os
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "senha")
DB_NAME = os.getenv("DB_NAME", "radar_macro")

def buscar_informacao_openai():
    pergunta = "Qual a visão do comitê sobre as contas públicas e o cenário fiscal?"
    
    data_corte = "2024-01-01" 
    
    print(f"Pergunta: '{pergunta}'")
    print(f"Filtro Ativo: Documentos publicados a partir de {data_corte}\n")

    print("1. Acessando OpenAI para traduzir a pergunta para vetor (1536 dimensões)...")
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=pergunta
    )
    vetor_pergunta = response.data[0].embedding

    print("2. Conectando ao PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )
    cur = conn.cursor()

    print("3. Realizando a Busca Híbrida (Vetor + Filtro SQL)...")
    query = """
        SELECT conteudo, data_publicacao, fonte, tipo_documento 
        FROM documentos_copom 
        WHERE data_publicacao >= %s
        ORDER BY embedding <=> %s::vector 
        LIMIT 3;
    """
    
    cur.execute(query, (data_corte, vetor_pergunta))
    resultados = cur.fetchall()

    print("\n--- RESULTADOS ENCONTRADOS (Busca Híbrida) ---\n")
    for i, (conteudo, data_pub, fonte, tipo) in enumerate(resultados, 1):
        print(f"🔹 TRECHO {i} | {fonte} - {tipo} | Data: {data_pub}")
        print(conteudo.strip())
        print("-" * 70)

    cur.close()
    conn.close()
    print("\nBusca validada com sucesso.")

if __name__ == "__main__":
    buscar_informacao_openai()
