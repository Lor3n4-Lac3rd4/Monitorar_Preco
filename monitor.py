#Principal sistema de monitoramento de preços

import time
import json
from datetime import datetime
from extrator_precos import ExtratorPrecos
from notificador import Notificador

class MonitorPrecos:
    def __init__(self):
        self.extrator = ExtratorPrecos()
        self.notificador = Notificador()
        self.historico = []
    
    def carregar_produtos(self, arquivo='produtos.json'):
        """Carrega lista de produtos do arquivo JSON"""
        try:
            with open(arquivo, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Arquivo de produtos não encontrado")
            return []
    
    def salvar_historico(self, produto, preco, url):
        """Salva histórico de preços"""
        registro = {
            'data': datetime.now().isoformat(),
            'produto': produto,
            'preco': preco,
            'url': url
        }
        
        self.historico.append(registro)
        
        try:
            with open('historico_precos.json', 'w') as f:
                json.dump(self.historico, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erro ao salvar histórico: {e}")
    
    def monitorar_produto(self, url, preco_desejado, nome_produto="", intervalo=3600):
        """Monitora um único produto"""
        if not nome_produto:
            nome_produto = self._extrair_nome_produto(url)
        
        print(f"\n🔍 Iniciando monitoramento: {nome_produto}")
        print(f"🎯 Preço desejado: R$ {preco_desejado:.2f}")
        print(f"🌐 URL: {url}")
        print("-" * 60)
        
        while True:
            preco_atual = self.extrator.extrair_preco(url)
            
            if preco_atual:
                self.salvar_historico(nome_produto, preco_atual, url)
                
                print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                print(f"💰 Preço atual: R$ {preco_atual:.2f}")
                
                if preco_atual <= preco_desejado:
                    self.notificador.enviar_notificacao_console(nome_produto, preco_atual, preco_desejado)
                    # self.notificador.enviar_email(nome_produto, preco_atual, preco_desejado, url)
                    break
                else:
                    diferenca = preco_atual - preco_desejado
                    print(f"💤 Ainda R$ {diferenca:.2f} acima do desejado")
            else:
                print("❌ Não foi possível obter o preço")
            
            print(f"⏳ Próxima verificação em {intervalo//60} minutos...")
            print("-" * 60)
            time.sleep(intervalo)
    
    def monitorar_lista(self, arquivo_produtos='produtos.json'):
        """Monitora uma lista de produtos"""
        produtos = self.carregar_produtos(arquivo_produtos)
        
        if not produtos:
            print("❌ Nenhum produto para monitorar")
            return
        
        print(f"🚀 Iniciando monitoramento de {len(produtos)} produtos")
        
        while True:
            for produto in produtos:
                try:
                    url = produto['url']
                    preco_desejado = produto['preco_desejado']
                    nome = produto.get('nome', self._extrair_nome_produto(url))
                    
                    preco_atual = self.extrator.extrair_preco(url)
                    
                    if preco_atual:
                        self.salvar_historico(nome, preco_atual, url)
                        
                        if preco_atual <= preco_desejado:
                            self.notificador.enviar_notificacao_console(nome, preco_atual, preco_desejado)
                            # self.notificador.enviar_email(nome, preco_atual, preco_desejado, url)
                        else:
                            print(f"💤 {nome} - R$ {preco_atual:.2f} (desejado: R$ {preco_desejado:.2f})")
                    else:
                        print(f"❌ {nome} - Preço não encontrado")
                        
                except Exception as e:
                    print(f"⚠️ Erro ao monitorar produto: {e}")
            
            print(f"⏳ Próxima verificação em 30 minutos...")
            time.sleep(1800)  # 30 minutos
    
    def _extrair_nome_produto(self, url):
        """Extrai um nome do produto da URL"""
        return url.split('/')[-1][:50]