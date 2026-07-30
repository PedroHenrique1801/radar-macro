import os
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres") 
DB_PASS = os.getenv("DB_PASSWORD", "senha") 
DB_NAME = os.getenv("DB_NAME", "radar_macro")

DATA_PUBLICACAO = "2024-06-19" 
FONTE = "BCB"
TIPO_DOCUMENTO = "Ata do Copom"

def processar_documento_openai():
    print("1. Lendo o documento da Ata do Copom...")
    try:
        with open("ata_copom_263.txt", "r", encoding="utf-8") as f:
            texto_completo = f.read()
    except FileNotFoundError:
        print("Erro: Arquivo 'ata_copom_263.txt' não encontrado. Rode o script de coleta primeiro.")
        return

    print("2. Fatiando o texto (Text Splitting)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_text(texto_completo)
    print(f"Texto dividido em {len(chunks)} blocos semânticos.")

    print("3. Conectando ao PostgreSQL e configurando pgvector...")
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()

    register_vector(conn)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS documentos_copom (
            id SERIAL PRIMARY KEY,
            conteudo TEXT,
            embedding vector(1536),
            data_publicacao DATE,
            fonte TEXT,
            tipo_documento TEXT
        );
    """)
    
    cur.execute("TRUNCATE TABLE documentos_copom RESTART IDENTITY;")
    conn.commit()

    print("4. Gerando Embeddings (OpenAI text-embedding-3-small) e salvando no PostgreSQL...")
    for i, chunk in enumerate(chunks):
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        vetor = response.data[0].embedding
        
        cur.execute(
            """
            INSERT INTO documentos_copom 
            (conteudo, embedding, data_publicacao, fonte, tipo_documento) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (chunk, vetor, DATA_PUBLICACAO, FONTE, TIPO_DOCUMENTO)
        )
        
        if (i + 1) % 10 == 0:
            print(f"   Processados {i + 1} de {len(chunks)} blocos...")

    conn.commit()
    cur.close()
    conn.close()

    print("\nSucesso! Ata do Copom fatiada, vetorizada (1536 dimensões via OpenAI) e salva no PostgreSQL.")

if __name__ == "__main__":
    processar_documento_openai()