import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        print("Tentando conectar ao PostgreSQL...")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        print("Conexão bem-sucedida!\n")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS teste_vector (
                id SERIAL PRIMARY KEY,
                texto TEXT,
                embedding VECTOR(3)
            );
        """)
        
        cur.execute("""
            INSERT INTO teste_vector (texto, embedding) 
            VALUES ('Isso é um teste do Radar Macro', '[0.1, 0.2, 0.3]');
        """)
        
        cur.execute("SELECT * FROM teste_vector;")
        resultado = cur.fetchone()
        print(f"Dado lido do banco: {resultado}")
        
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao conectar ou executar: {e}")

if __name__ == "__main__":
    test_connection()