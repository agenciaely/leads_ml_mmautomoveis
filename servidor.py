from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os

app = Flask(__name__)

# Configuração do Google Sheets
SHEET_ID = os.getenv("SHEET_ID")  

# Carregar credenciais do ambiente (Render)
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")  
CREDENTIALS = json.loads(GOOGLE_CREDENTIALS)  

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(CREDENTIALS, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1 

@app.route("/")
def home():
    return "Servidor Flask rodando!", 200

@app.route("/webhook", methods=["POST"])
def receber_lead():
    data = request.json

    # ✅ LOG para verificar o que o Mercado Livre está enviando
    print("📩 Dados Recebidos do Mercado Livre:", data)

    # Salvar os dados recebidos em um arquivo de log no servidor para análise
    with open("log_mercado_livre.txt", "a") as log_file:
        log_file.write(json.dumps(data, indent=4) + "\n")

    # Captura a data/hora exata da requisição
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pegando informações do lead com valores padrão
    lead_name = data.get("name", "Desconhecido")
    phone = data.get("phone", "Não informado")
    vehicle = data.get("vehicle", "Não informado")
    date = data.get("date", "Não informado")
    cpf = data.get("cpf", "Não informado")
    question = data.get("question", "Nenhuma pergunta feita")
    financing_requested = "Sim" if data.get("financing_requested") else "Não"
    whatsapp_clicked = "Sim" if data.get("whatsapp_clicked") else "Não"
    source = "Mercado Livre"

    # Criando a linha de dados na ordem correta
    lead = [
        timestamp,        # Coluna A - Data/Hora
        lead_name,        # Coluna B - Nome
        phone,            # Coluna C - Telefone
        vehicle,          # Coluna D - Veículo
        date,             # Coluna E - Data de Interesse
        cpf,              # Coluna F - CPF
        question,         # Coluna G - Pergunta Feita
        financing_requested,  # Coluna H - Solicitou Financiamento?
        whatsapp_clicked,     # Coluna I - Clicou no WhatsApp?
        source            # Coluna J - Origem do Lead
    ]

    # Adicionar os dados na planilha
    sheet.append_row(lead, value_input_option="RAW")

    return jsonify({"message": "Lead salvo no Google Sheets!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
