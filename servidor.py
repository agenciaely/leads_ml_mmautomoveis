from flask import Flask, request, jsonify
import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configuração do Google Sheets
SHEET_ID = os.getenv("SHEET_ID")  # ID da sua planilha do Google Sheets
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS")  # Credenciais do Google em formato JSON

# Verifica se as credenciais foram carregadas corretamente
if not CREDENTIALS_JSON:
    raise ValueError("As credenciais do Google não foram carregadas. Verifique as variáveis de ambiente.")

# Autenticação com Google Sheets usando as credenciais do ambiente
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(CREDENTIALS_JSON)  # Converte a string JSON em um dicionário Python
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1  # Usamos a primeira aba da planilha

@app.route("/")
def home():
    return "Servidor Flask rodando!", 200

@app.route("/webhook", methods=["POST"])
def receber_lead():
    data = request.json

    lead = [
        data.get("name"),
        data.get("phone"),
        data.get("vehicle"),
        data.get("date"),
        "Mercado Livre"
    ]

    # Adicionar os dados na planilha
    sheet.append_row(lead)

    return jsonify({"message": "Lead salvo no Google Sheets!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
