from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests

def criar_pasta(nome_da_pasta):
    try:
        if os.path.exists(nome_da_pasta):
            print(f"Já existe uma pasta com o nome {nome_da_pasta}")
        else:
            os.mkdir(nome_da_pasta)
    except OSError:
        print("Não foi possível criar um arquivo")

driver = webdriver.Chrome()
url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
driver.get(url)



table=driver.find_element(By.TAG_NAME,"table")
tbody = table.find_element(By.TAG_NAME,"tbody")
tds = tbody.find_elements(By.TAG_NAME,"td")


arquivo_csv=[]

for td in tds:
    try:
        a_tag = td.find_element(By.TAG_NAME,"a")
        href = a_tag.get_attribute("href")
        if href and href.endswith("csv"):
            arquivo_csv.append(href)
    except:
        continue
    
driver.quit()

for csv in arquivo_csv:
    print(f"arquivo encotrado : {csv} ")

arquivo_baixado=[]

pasta_dowload="./task_3/pasta_csv"

criar_pasta(pasta_dowload)

for baixar_csv in arquivo_csv:
    nome_arquivo = baixar_csv.split("/")[-1]
    caminho_arquivo = os.path.join(pasta_dowload, nome_arquivo)

    print(f"Baixando {nome_arquivo} ...")
    resposta = requests.get(baixar_csv, stream=True)
    with open(caminho_arquivo, "wb") as arquivo:
        for chunk in resposta.iter_content(chunk_size=8192):
            arquivo.write(chunk)

    arquivo_baixado.append(caminho_arquivo)

print("Arquivo Csv Baixado com Sucesso")