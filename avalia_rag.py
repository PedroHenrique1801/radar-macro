import psycopg2
from sentence_transformers import SentenceTransformer

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "radar"
DB_PASS = "radar123"
DB_NAME = "radar_macro"
DATA_CORTE = "2024-01-01"

def rodar_avaliacao():
    perguntas = [
        "Qual é a atual meta para a inflação?",
        "Como o comitê avalia o cenário econômico global?",
        "Quais foram os comentários sobre o mercado de trabalho e desemprego?",
        "Há alguma menção sobre a evolução do IPCA?",
        "Qual foi a decisão final sobre a taxa Selic nesta reunião?",
        "Quais são os principais riscos de alta para a inflação?",
        "Como estão as expectativas de inflação para 2025?",
        "Qual a avaliação sobre a atividade econômica doméstica?",
        "Houve comentários sobre a política fiscal ou contas públicas?",
        "Como os conflitos geopolíticos estão afetando a economia?"
    ]

    print("Carregando modelo de IA para os testes...\n")
    modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME
    )
    cur = conn.cursor()

    query = """
        SELECT conteudo 
        FROM documentos_copom 
        WHERE data_publicacao >= %s
        ORDER BY embedding <=> %s::vector 
        LIMIT 3;
    """

    acertos_estimados = 0

    print(f"{'='*60}")
    print(" INICIANDO BATERIA DE AVALIAÇÃO (TOP-3)".center(60))
    print(f"{'='*60}\n")

    for i, pergunta in enumerate(perguntas, 1):
        print(f"[{i}/10] 🗣️ PERGUNTA: {pergunta}")
        
        vetor_pergunta = modelo.encode(pergunta).tolist()
        cur.execute(query, (DATA_CORTE, vetor_pergunta))
        resultados = cur.fetchall()

        for j, (conteudo,) in enumerate(resultados, 1):
            trecho_curto = conteudo.replace('\n', ' ')[:120] + "..."
            print(f"   {j}º -> {trecho_curto}")
        
        print("-" * 60)

    cur.close()
    conn.close()

if __name__ == "__main__":
    rodar_avaliacao()