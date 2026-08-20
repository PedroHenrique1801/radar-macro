import requests
import PyPDF2
import io

def coletar_ata_copom():  
    print("Iniciando o download da Ata do Copom...")
    
    url_ata = "https://www.bcb.gov.br/content/copom/atascopom/Copom263-not20240619263.pdf"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        response = requests.get(url_ata, headers=headers)
        response.raise_for_status()
        print("Download concluído! Extraindo texto...")
        
        arquivo_pdf = io.BytesIO(response.content)
        leitor = PyPDF2.PdfReader(arquivo_pdf)
        
        texto_completo = ""
        for pagina in leitor.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"
        
        print(f"\nSucesso! O documento possui {len(leitor.pages)} páginas.")
        print("\n--- Primeiros 500 caracteres da Ata ---")
        print(texto_completo[:500])
        print("---------------------------------------\n")
        
        arquivo_saida = "ata_copom_263.txt"
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write(texto_completo)
            
        print(f"Arquivo '{arquivo_saida}' criado com sucesso na raiz do projeto!")

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao baixar o PDF: {e}")
    except Exception as e:
        print(f"Ocorreu um erro na extração do texto: {e}")

if __name__ == "__main__":
    coletar_ata_copom()
