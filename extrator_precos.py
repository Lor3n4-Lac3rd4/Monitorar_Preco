# extrator_precos.py

import requests
import re
import random
import time
from bs4 import BeautifulSoup
from config import HEADERS, SELETORES_SITES, USER_AGENTS

class ExtratorPrecos:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def identificar_site(self, url):
        """Identifica qual site é pela URL"""
        if 'amazon.com.br' in url:
            return 'AMAZON'
        elif 'mercadolivre.com.br' in url:
            return 'MERCADO_LIVRE'
        elif 'webmotors.com.br' in url:
            return 'WEBMOTORS'
        elif 'olx.com.br' in url:
            return 'OLX'
        elif 'magazineluiza.com.br' in url:
            return 'MAGAZINE_LUIZA'
        elif 'americanas.com.br' in url:
            return 'AMERICANAS'
        elif 'submarino.com.br' in url:
            return 'SUBMARINO'
        else:
            return 'GENERICO'
    
    def extrair_preco(self, url):
        """Extrai preço baseado no site"""
        try:
            site = self.identificar_site(url)
            print(f"🔍 Identificado: {site}")
            
            # Rotação de User-Agent
            headers = self.session.headers.copy()
            headers['User-Agent'] = random.choice(USER_AGENTS)
            
            # Delay aleatório entre requisições
            time.sleep(random.uniform(2, 5))
            
            # Faz a requisição
            response = self.session.get(
                url, 
                timeout=15,
                allow_redirects=True,
                headers=headers
            )
            
            # Verifica o status
            if response.status_code == 403:
                print("❌ ERRO 403 - Acesso proibido (site está bloqueando)")
                return None
            elif response.status_code == 404:
                print("❌ ERRO 404 - Página não encontrada")
                return None
            elif response.status_code == 500:
                print("❌ ERRO 500 - Erro interno do servidor")
                print("💡 Dica: Tente outro site ou aguarde alguns minutos")
                return None
            elif response.status_code != 200:
                print(f"⚠️ Status code: {response.status_code}")
                return None
            
            # Encoding
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Tenta pelos seletores específicos do site
            if site in SELETORES_SITES:
                preco = self._extrair_por_seletores(soup, SELETORES_SITES[site])
                if preco:
                    return preco
            
            # Fallback: busca genérica
            preco_generico = self._extrair_preco_generico(soup)
            if preco_generico:
                return preco_generico
            
            print("🔍 Nenhum preço encontrado na página")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conexão: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return None

    # ... (o resto das funções permanece igual) ...

    def _extrair_por_seletores(self, soup, seletores):
        """Tenta extrair preço usando seletores CSS"""
        for seletor in seletores:
            elemento = soup.select_one(seletor)
            if elemento:
                preco_texto = elemento.get_text().strip()
                preco = self._limpar_preco(preco_texto)
                if preco:
                    print(f"💰 Preço encontrado via seletor: R$ {preco:.2f}")
                    return preco
        return None
    
    def _extrair_preco_generico(self, soup):
        """Busca genérica por preços no HTML"""
        # Procura por elementos com "R$"
        elementos_reais = soup.find_all(text=re.compile(r'R\$\s*\d+'))
        
        for elemento in elementos_reais:
            preco = self._limpar_preco(elemento)
            if preco:
                print(f"💰 Preço encontrado genérico: R$ {preco:.2f}")
                return preco
        
        return None
    
    def _limpar_preco(self, texto_preco):
        """Converte texto do preço para float"""
        try:
            # Remove caracteres não numéricos, exceto ponto e vírgula
            texto_limpo = re.sub(r'[^\d,.]', '', texto_preco)
            
            # Se terminar com vírgula e dois dígitos, assume que é decimal
            if re.match(r'^\d+,\d{2}$', texto_limpo):
                return float(texto_limpo.replace(',', '.'))
            
            # Se tiver ponto como separador de milhar e vírgula como decimal
            if '.' in texto_limpo and ',' in texto_limpo:
                partes = texto_limpo.split(',')
                if len(partes) == 2 and len(partes[1]) == 2:  # Centavos
                    inteiro = partes[0].replace('.', '')
                    return float(f"{inteiro}.{partes[1]}")
            
            # Tenta converter diretamente
            return float(texto_limpo.replace(',', '.'))
            
        except (ValueError, AttributeError):
            return None

    def testar_extracao(self, url):
        """Testa a extração de preço de uma URL"""
        print(f"🧪 Testando extração: {url}")
        preco = self.extrair_preco(url)
        
        if preco:
            print(f"✅ Preço encontrado: R$ {preco:.2f}")
        else:
            print("❌ Preço não encontrado")
        
        return preco