from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Configuração do Google Sheets
SHEET_ID = "1idSwyvj6B-pVA0DQ2D9Tc7R8fq6PnJHcMR4EkkC-4Hg"  # ID da sua planilha
CREDENTIALS_FILE = r"C:\Users\Usuario\Documents\Python\MM Automoveis\Integrações\importar\credentials.json"

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
