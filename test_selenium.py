from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO
import pandas as pd

# Inicializar o driver do Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL do site que será acessado
url = 'https://www.fundamentus.com.br/resultado.php'

# Acessar o site
driver.get(url)

# Localizar a tabela no HTML da página
local_tabela = '/html/body/div[1]/div[2]/table'
elemento = driver.find_element("xpath", local_tabela)

# Obter o HTML da tabela
html_tabela = elemento.get_attribute('outerHTML')

# Envolver o HTML em um objeto StringIO
html_buffer = StringIO(html_tabela)

# Ler a tabela a partir do HTML
tabela = pd.read_html(html_buffer, thousands='.', decimal=',')[0]

# Definir o índice da tabela como "Papel"
tabela = tabela.set_index("Papel")

# Selecionar colunas de interesse
tabela = tabela[['Cotação', 'EV/EBIT', 'ROIC', 'Liq.2meses']]

# Limpeza e conversão da coluna ROIC
tabela['ROIC'] = tabela['ROIC'].str.replace("%", "")
tabela['ROIC'] = tabela['ROIC'].str.replace(".", "")
tabela['ROIC'] = tabela['ROIC'].str.replace(",", ".")
tabela['ROIC'] = tabela['ROIC'].astype(float)

# Filtragem da tabela
tabela = tabela[tabela['Liq.2meses'] > 1000000]
tabela = tabela[tabela['EV/EBIT'] > 0]
tabela = tabela[tabela['ROIC'] > 0]

# Calcular rankings
tabela['ranking_ev_ebit'] = tabela['EV/EBIT'].rank(ascending=True)
tabela['ranking_roic'] = tabela['ROIC'].rank(ascending=False)
tabela['ranking_total'] = tabela['ranking_ev_ebit'] + tabela['ranking_roic']

# Ordenar a tabela pelos rankings
tabela = tabela.sort_values('ranking_total')

# Salvar a tabela em um arquivo CSV
tabela.to_csv('tabela_ranking.csv')

# Salvar a tabela em um arquivo Excel
tabela.to_excel('tabela_ranking.xlsx')

# Exibir as 100 primeiras linhas da tabela
print(tabela.head(100))

# Fechar o driver
driver.quit()
