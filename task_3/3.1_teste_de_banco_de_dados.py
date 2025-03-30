import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import zipfile
import os
from datetime import datetime

def criar_pasta(nome_da_pasta):
    try:
        if os.path.exists(nome_da_pasta):
            print(f"Já existe uma pasta com o nome {nome_da_pasta}")
        else:
            os.mkdir(nome_da_pasta)
    except OSError:
        print("Não foi possível criar um arquivo")

data=datetime.now().year
data_anos=[]

for i in range(1,3):
    ano=data-i
    data_anos.append(ano)

driver = webdriver.Chrome()
url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
driver.get(url)

links_encontrados = []

for ano_buscado in data_anos:


    link_ano = driver.find_element(By.LINK_TEXT, f"{ano_buscado}/")
    link_ano.click()
    table = driver.find_element(By.TAG_NAME, "table")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    tds = tbody.find_elements(By.TAG_NAME, "td")

    for td in tds:
        try:
            a_tag = td.find_element(By.TAG_NAME, "a")
            href = a_tag.get_attribute('href')
            if href and href.endswith(".zip"):
                links_encontrados.append(href)
        except:
            continue

    driver.back() 

driver.quit()

print(f"Dos anos {data_anos} : Foram encontrados {len(links_encontrados)} arquivos ZIP.")
for link in links_encontrados:
    print(link)

pasta_dowload="./task_3/arquivos_zip"

criar_pasta(pasta_dowload)

arquivos_baixados = []


for link in links_encontrados:
    nome_arquivo = link.split("/")[-1]
    caminho_arquivo = os.path.join(pasta_dowload, nome_arquivo)

    print(f"Baixando {nome_arquivo} ...")
    resposta = requests.get(link, stream=True)
    with open(caminho_arquivo, "wb") as arquivo:
        for chunk in resposta.iter_content(chunk_size=8192):
            arquivo.write(chunk)

    arquivos_baixados.append(caminho_arquivo)

print("\nDownload concluído!")

print("Deseja Descompactar os Arquivos baixados ?")
descompatar=input("Resposta S/N: ").lower()

if (descompatar == "s"):
    for arquivo_zip in arquivos_baixados:
        try:
            with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
                zip_ref.extractall("./task_3/arquivos_descompactados")
            print(f"{arquivo_zip} descompactado.")
        except zipfile.BadZipFile:
            print(f"{arquivo_zip} não é um arquivo zip válido.")
else:
    print("Arquivos baixados com sucesso")
