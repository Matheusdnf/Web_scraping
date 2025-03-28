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


# Clicar no link 2023/
for click_ano in data_anos:
    try:
        link_ano = driver.find_element(By.LINK_TEXT, f"{click_ano}/")
        link_ano.click()
        table = driver.find_element(By.TAG_NAME, "table")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        tds = tbody.find_elements(By.TAG_NAME, "td")

        links = []
        for td in tds:
            try:
                a_tag = td.find_element(By.TAG_NAME, "a")
                href = a_tag.get_attribute('href')
                if href and href.endswith(".zip"):
                    links.append(href)
            except:
                continue

        print(f"{click_ano}: {len(links)} arquivos zip encontrados.")
        for link in links:
            print(link)

        driver.back()  # Voltar só depois de capturar os links

    except Exception as e:
        print(f"Erro ao acessar o ano {click_ano}: {e}")

# Criar pasta downloads
os.makedirs("downloads", exist_ok=True)

arquivos_baixados = []

for link in links:
    nome_arquivo = link.split("/")[-1]
    caminho_arquivo = os.path.join("downloads", nome_arquivo)

    print(f"Baixando {nome_arquivo} ...")
    resposta = requests.get(link, stream=True)
    with open(caminho_arquivo, "wb") as arquivo:
        for chunk in resposta.iter_content(chunk_size=8192):
            arquivo.write(chunk)

    arquivos_baixados.append(caminho_arquivo)

print("\nDownload concluído!")

# (Opcional) Descompactar
for arquivo_zip in arquivos_baixados:
    try:
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall("downloads")
        print(f"{arquivo_zip} descompactado.")
    except zipfile.BadZipFile:
        print(f"{arquivo_zip} não é um arquivo zip válido.")

driver.quit()
