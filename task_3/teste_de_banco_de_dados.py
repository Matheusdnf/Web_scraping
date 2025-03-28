import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import zipfile
import os
from datetime import datetime

data=datetime.now().year
data_anos=[]

#Pegar os último 2 anos com base no ano atual
for i in range(1,3):
    ano=data-i
    data_anos.append(ano)

driver = webdriver.Chrome()
url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
driver.get(url)


for ano_buscado in data_anos:
    try:
        link_ano = driver.find_element(By.LINK_TEXT, f"{ano_buscado}/")
        link_ano.click()
        table = driver.find_element(By.TAG_NAME, "table")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        tds = tbody.find_elements(By.TAG_NAME, "td")

        links_encontrados = []
        for td in tds:
            try:
                a_tag = td.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute('href')
                if href and href.endswith(".zip"):
                    links_encontrados.append(href)
            except:
                continue

        print(f"{ano_buscado} : Foram encontrados {len(links_encontrados)} arquivos ZIP.")
        for link in links_encontrados:
            print(link)

        driver.back() 

    except Exception as e:
        print(f"Erro ao acessar o ano {ano_buscado}: {e}")

driver.quit()

pasta_dowload="./task_3/pasta_dowloads"
try:
    if os.path.exists(pasta_dowload):
        print(f"Já existe uma pasta com o nome {pasta_dowload}")
    else:
        os.mkdir(pasta_dowload)
except OSError:
    print("Não foi possível criar um arquivo")


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
descompatar=input("Resposta S/N").lower()
pasta="Arquivos_Compactados"
try:
    if os.path.exists(pasta):
        print(f"Já existe uma pasta com o nome {pasta}")
    else:
        os.mkdir(pasta)
except OSError:
    print("Não foi possível criar um arquivo")

os.makedirs("arquivos_compactados", exist_ok=True)
if (descompatar == "s"):
    for arquivo_zip in arquivos_baixados:
        try:
            with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
                zip_ref.extractall("./task_3/downloads")
            print(f"{arquivo_zip} descompactado.")
        except zipfile.BadZipFile:
            print(f"{arquivo_zip} não é um arquivo zip válido.")
else:
    print("Arquivos baixados com sucesso")
