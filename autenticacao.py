import requests

# Substitua pelos seus dados do Mercado Livre
CLIENT_ID = "3359470866976597"
CLIENT_SECRET = "oHZ8soxT1OZK29L173stYop8Z0AiIl5z"
REDIRECT_URI = "https://2815-2804-47e4-8843-1f00-25a8-ef39-60ab-9a79.ngrok-free.app"  # Precisa ser HTTPS válido

# Passo 1: Obter o Código de Autorização (manual)
print(f"Acesse este link e autorize o aplicativo: \n\nhttps://auth.mercadolivre.com.br/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}")

AUTH_CODE = input("\nCole aqui o código de autorização: ")

# Passo 2: Trocar o código pelo Access Token
url = "https://api.mercadolibre.com/oauth/token"

data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTH_CODE,
    "redirect_uri": REDIRECT_URI
}

response = requests.post(url, data=data)
token_info = response.json()

if "access_token" in token_info:
    print("\n✅ Access Token gerado com sucesso!")
    print("Access Token:", token_info["access_token"])
else:
    print("\n❌ Erro ao gerar Access Token:", token_info)
