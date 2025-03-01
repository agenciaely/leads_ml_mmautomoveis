from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

# Caminho para o driver do Edge (verifique se está correto)
EDGE_DRIVER_PATH = r"C:\WebDriver\msedgedriver.exe"

# Configurar o Edge para conectar à sessão aberta
options = webdriver.EdgeOptions()
options.debugger_address = "localhost:9222"  # Porta usada pelo WebDriver

# Iniciar o navegador
service = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

# Acessar a página do Mercado Livre
url = "https://www.mercadolivre.com.br/pessoas-interessadas?index=2&filters=NOT_CONTACTED"
driver.get(url)
time.sleep(5)  # Espera para garantir o carregamento da página

# Fechar o navegador após testar
# driver.quit()
