from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# Configuração do Google Sheets
SHEET_ID = "1idSwyvj6B-pVA0DQ2D9Tc7R8fq6PnJHcMR4EkkC-4Hg"
CREDENTIALS_FILE = "credentials.json"  # Arquivo de credenciais armazenado no Render

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1  # Usamos a primeira aba da planilha

@app.route("/")
def home():
    return "Servidor Flask rodando!", 200

@app.route("/webhook", methods=["POST"])
def receber_lead():
    data = request.json

    # Pegando informações do lead
    lead_name = data.get("name", "Desconhecido")
    phone = data.get("phone", "Não informado")
    vehicle = data.get("vehicle", "Não informado")
    cpf = data.get("cpf", "Não informado")  # Adicionando CPF
    question = data.get("question", "Nenhuma pergunta feita")  # Pergunta realizada
    financing = data.get("financing", "Não informado")  # Se simulou financiamento
    contact_whatsapp = data.get("whatsapp", "Não entrou")  # Se entrou em contato via WhatsApp

    # Registrando a data e hora do recebimento
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Adicionar os dados na planilha
    lead = [timestamp, lead_name, phone, vehicle, cpf, question, financing, contact_whatsapp, "Mercado Livre"]
    sheet.append_row(lead)

    return jsonify({"message": "Lead salvo no Google Sheets!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
