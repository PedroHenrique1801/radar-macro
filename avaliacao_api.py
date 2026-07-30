import requests
import time
import re

API_URL = "http://localhost:8080/api/rag/perguntar"

testes = [
    {
        "pergunta": "O que o comitê diz sobre o cenário internacional e as taxas de juros externas?",
        "fato_esperado": "Estados Unidos"
    },
    {
        "pergunta": "Quais são os alertas do comitê em relação às contas públicas e à política fiscal?",
        "fato_esperado": "sustentabilidade da dívida" 
    },
    {
        "pergunta": "Como o comitê avalia o estado atual do mercado de trabalho doméstico?",
        "fato_esperado": "mercado de trabalho apertado"
    },
    {
        "pergunta": "Qual é a situação das expectativas de inflação segundo a pesquisa Focus?",
        "fato_esperado": "desancoragem"
    },
    {
        "pergunta": "O que o documento menciona sobre a trajetória da inflação cheia ao consumidor?",
        "fato_esperado": "desinflação"
    },
    {
        "pergunta": "Qual foi a conclusão sobre a postura da política monetária para as próximas reuniões?",
        "fato_esperado": "contracionista"
    },
    {
        "pergunta": "Quais são as premissas para a taxa de câmbio e o preço do petróleo no cenário de referência?",
        "fato_esperado": "paridade do poder de compra"
    },
    {
        "pergunta": "Há alguma menção sobre a resiliência na inflação de serviços?",
        "fato_esperado": "serviços"
    },
    {
        "pergunta": "Quais são as projeções de inflação apuradas para os anos de 2024 e 2025?",
        "fato_esperado": "4,0%"
    },
    {
        "pergunta": "Qual é o impacto do esmorecimento das reformas estruturais na economia?",
        "fato_esperado": "taxa de juros neutra"
    }
]

def avaliar_api():
    print("Iniciando avaliação formal do RAG via API...")
    acertos = 0
    total = len(testes)

    for i, teste in enumerate(testes, 1):
        pergunta = teste["pergunta"]
        fato_esperado = teste["fato_esperado"].lower()
        
        print(f"\n[{i}/{total}] Testando: {pergunta}")
        
        try:
            resposta = requests.post(API_URL, json={"pergunta": pergunta})
            resposta.raise_for_status()
            dados = resposta.json()
            
            texto_fontes = " ".join([fonte["conteudo"].lower() for fonte in dados.get("fontes", [])])
            
            texto_fontes = re.sub(r'\s+', ' ', texto_fontes)
            
            if fato_esperado in texto_fontes:
                print("✅ SUCESSO: Fato esperado encontrado nas fontes.")
                acertos += 1
            else:
                print(f"❌ FALHA: Fato esperado '{fato_esperado}' não encontrado.")
                print(f"   Contexto recuperado: {texto_fontes[:200]}...") 
                
        except Exception as e:
            print(f"ERRO de conexão ou execução: {e}")
            
        time.sleep(1) 

    taxa_acerto = (acertos / total) * 100
    print("\n" + "="*40)
    print(f"RESULTADO FINAL: {acertos}/{total} acertos ({taxa_acerto:.1f}%)")
    if taxa_acerto >= 70.0:
        print("META ATINGIDA! O pipeline de recuperação está excelente.")
    else:
        print("META NÃO ATINGIDA (Abaixo de 70%). Avaliar qualidade dos embeddings ou fragmentação dos PDFs.")
    print("="*40)

if __name__ == "__main__":
    avaliar_api()