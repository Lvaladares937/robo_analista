import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Configurações do Chrome para desabilitar a política de CORS
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--allow-running-insecure-content")

    # Inicia o navegador com as opções
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    print("Navegador iniciado com sucesso.")

    input("Pressione Enter para acessar a URL...")

    # Acessa a URL
    url = 'https://www.fundamentus.com.br/resultado.php'
    driver.get(url)
    print("URL acessada com sucesso.")

    # Espera até que a tabela esteja presente na página
    wait = WebDriverWait(driver, 10)
    local_tabela = '/html/body/div[1]/div[2]/table'
    elemento = wait.until(EC.presence_of_element_located((By.XPATH, local_tabela)))

    # Desce a página até o final para carregar todos os dados
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Ajuste o tempo conforme necessário

    # Obtém o HTML da tabela
    html_tabela = elemento.get_attribute("outerHTML")
    print("Tabela obtida com sucesso.")

    input("Pressione Enter para obter dados via POST...")

    # URL da requisição POST (ajuste conforme necessário)
    post_url = 'https://www.strongyloides.com.br/pv.php'

    # Cabeçalhos da requisição POST
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Referer': 'https://www.fundamentus.com.br/',
    }

    # Corpo da requisição POST (ajuste conforme necessário)
    data = {
        'u': '1',
        'i': ''
    }

    # Faz a requisição POST
    response = requests.post(post_url, headers=headers, data=data)
    response.raise_for_status()  # Verifica se houve erro na requisição

    # Salva o conteúdo da resposta em um arquivo para análise
    with open('resposta_post.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

    # Exibe o conteúdo completo da resposta para verificação
    print("Status Code da requisição POST:", response.status_code)
    print("Resposta salva em 'resposta_post.html'.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

input("Pressione Enter para fechar o navegador...")

# Fecha o navegador
driver.quit()
