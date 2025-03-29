import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome
url="https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
driver.get(url)

arquivo_csv=[]

table=driver.find_element(By.TAG_NAME,"table")
tbody = table.find_element(By.TAG_NAME,"tbody")
tr = tbody.find_elements(By.TAG_NAME,"tr")
th = tr.find_elements(By.TAG_NAME,"th")
a_tag = th.find_elements(By.TAG_NAME,"a")
href = a_tag.get_attribute('href')
if href and href.endswith("csv"):
    arquivo_csv.append(href)
else:
    print("Nenhum Arquivo CSV encontrado")


    


