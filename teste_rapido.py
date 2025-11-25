# teste_rapido.py
import requests
from bs4 import BeautifulSoup

def testar_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"🔍 Testando: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Procura preços genéricos
            import re
            textos_preco = soup.find_all(string=re.compile(r'R\$\s*\d+'))
            
            if textos_preco:
                for texto in textos_preco[:3]:  # Mostra os 3 primeiros
                    print(f"💰 Possível preço: {texto.strip()}")
            else:
                print("❌ Nenhum preço encontrado com 'R$'")
                
        else:
            print("❌ Página não carregou corretamente")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

# Teste com URLs curtas e funcionais
urls_teste = [
    "https://www.amazon.com.br",
    "https://www.mercadolivre.com.br", 
    "https://www.magazineluiza.com.br"
]

for url in urls_teste:
    testar_url(url)
    print("-" * 50)