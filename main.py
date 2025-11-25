# main.py

from monitor import MonitorPrecos
from extrator_precos import ExtratorPrecos

def main():
    monitor = MonitorPrecos()
    
    print("🛒 MONITOR DE PREÇOS AUTOMÁTICO")
    print("1. Monitorar um produto")
    print("2. Monitorar lista de produtos")
    print("3. Testar extração de preço")
    
    opcao = input("\nEscolha uma opção: ")
    
    if opcao == "1":
        url = input("URL do produto: ")
        preco_desejado = float(input("Preço desejado: R$ "))
        nome = input("Nome do produto (opcional): ")
        
        monitor.monitorar_produto(url, preco_desejado, nome)
    
    elif opcao == "2":
        monitor.monitorar_lista()
    
    elif opcao == "3":
        url = input("URL para testar: ")
        extrator = ExtratorPrecos()
        extrator.testar_extracao(url)  # CORRIGIDO: "testar" não "festar"
    
    else:
        print("❌ Opção inválida")

if __name__ == "__main__":
    main()