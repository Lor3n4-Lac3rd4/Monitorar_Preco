# app.py
from flask import Flask, render_template, request, jsonify
import json
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

# Estado global do monitoramento
monitor_status = {
    'ativo': False,
    'tipo': None,
    'ultima_atualizacao': None
}

logs = []

def adicionar_log(mensagem):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {mensagem}"
    logs.append(log_entry)
    # Mantém apenas os últimos 100 logs
    if len(logs) > 100:
        logs.pop(0)
    print(log_entry)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/testar-extracao', methods=['POST'])
def testar_extracao():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'success': False, 'message': 'URL é obrigatória'})
        
        adicionar_log(f"🧪 Testando extração: {url}")
        
        # Simulação de extração de preço (substitua pela sua lógica real)
        # preco = extrator.extrair_preco(url)
        preco = 199.90  # Valor simulado para teste
        
        if preco:
            mensagem = f"✅ Preço encontrado: R$ {preco:.2f}"
            adicionar_log(mensagem)
            return jsonify({
                'success': True, 
                'message': mensagem,
                'preco': preco
            })
        else:
            mensagem = "❌ Preço não encontrado"
            adicionar_log(mensagem)
            return jsonify({
                'success': False, 
                'message': mensagem
            })
            
    except Exception as e:
        mensagem = f"❌ Erro: {str(e)}"
        adicionar_log(mensagem)
        return jsonify({'success': False, 'message': mensagem})

@app.route('/iniciar-monitoramento', methods=['POST'])
def iniciar_monitoramento():
    try:
        data = request.get_json()
        produtos = data.get('produtos', [])
        
        if not produtos:
            return jsonify({'success': False, 'message': 'Nenhum produto para monitorar'})
        
        global monitor_status
        monitor_status['ativo'] = True
        monitor_status['tipo'] = 'lista'
        monitor_status['ultima_atualizacao'] = datetime.now().isoformat()
        
        # Simulação de monitoramento
        adicionar_log(f"🚀 Iniciando monitoramento de {len(produtos)} produtos")
        
        for produto in produtos:
            nome = produto.get('nome', 'Sem nome')
            adicionar_log(f"🔍 Monitorando: {nome}")
        
        return jsonify({'success': True, 'message': 'Monitoramento iniciado'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro: {str(e)}'})

@app.route('/parar-monitoramento', methods=['POST'])
def parar_monitoramento():
    global monitor_status
    monitor_status['ativo'] = False
    monitor_status['tipo'] = None
    adicionar_log("⏹️ Monitoramento parado")
    return jsonify({'success': True, 'message': 'Monitoramento parado'})

@app.route('/status')
def status():
    return jsonify(monitor_status)

@app.route('/logs')
def get_logs():
    return jsonify({'logs': logs})

@app.route('/produtos-exemplo')
def produtos_exemplo():
    exemplo = {
        "produtos": [
            {
                "nome": "Notebook Dell Inspiron 15",
                "url": "https://www.amazon.com.br/dp/B0C5VDLZ33",
                "preco_desejado": 2500.00
            },
            {
                "nome": "Moto Yamaha MT-09 2024", 
                "url": "https://www.mercadolivre.com.br/moto-yamaha-mt-09-2024-890cc/p/MLB19863258",
                "preco_desejado": 45000.00
            }
        ]
    }
    return jsonify(exemplo)

if __name__ == '__main__':
    # Cria a pasta de templates se não existir
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static/css'):
        os.makedirs('static/css')
    if not os.path.exists('static/js'):
        os.makedirs('static/js')
    
    print("🚀 Iniciando servidor Flask...")
    print("📧 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)