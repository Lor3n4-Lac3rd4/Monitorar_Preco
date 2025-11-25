#sistema de notificação

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_CONFIG

class Notificador:
    def __init__(self):
        self.config = EMAIL_CONFIG
    
    def enviar_email(self, produto, preco_atual, preco_desejado, url):
        """Envia notificação por email quando o preço baixa"""
        try:
            msg = MIMEMultipart()
            msg['Subject'] = f'🎉 ALERTA DE PREÇO - {produto}'
            msg['From'] = self.config['email']
            msg['To'] = self.config['email']  # ou outro destinatário
            
            corpo = f"""
            <h2>🎉 Preço Baixou! 🎉</h2>
            
            <p><strong>Produto:</strong> {produto}</p>
            <p><strong>Preço Atual:</strong> R$ {preco_atual:.2f}</p>
            <p><strong>Preço Desejado:</strong> R$ {preco_desejado:.2f}</p>
            <p><strong>Economia:</strong> R$ {(preco_atual - preco_desejado):.2f}</p>
            
            <p><a href="{url}">COMPRAR AGORA</a></p>
            
            <hr>
            <small>Monitor de Preços Automático</small>
            """
            
            msg.attach(MIMEText(corpo, 'html'))
            
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['email'], self.config['senha'])
                server.send_message(msg)
            
            print("✅ Email de notificação enviado!")
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
    
    def enviar_notificacao_console(self, produto, preco_atual, preco_desejado):
        """Notificação simples no console"""
        print("\n" + "🎉" * 20)
        print(f"🎉 PREÇO BAIXOU! 🎉")
        print(f"🎉 Produto: {produto}")
        print(f"🎉 Preço Atual: R$ {preco_atual:.2f}")
        print(f"🎉 Preço Desejado: R$ {preco_desejado:.2f}")
        print(f"🎉 Economia: R$ {(preco_atual - preco_desejado):.2f}")
        print("🎉" * 20 + "\n")