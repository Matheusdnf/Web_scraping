import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import zipfile
import os

pasta="pdfs"
try:
    if os.path.isfile(pasta):
        print(f"Já existe uma pasta com o nome {pasta}")
    else:
        os.mkdir(pasta)
except OSError:
    print("Não foi possível criar um arquivo")

driver = webdriver.Chrome()
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
driver.get(url)

div = driver.find_element(By.CLASS_NAME,"cover-richtext-tile.tile-content")

ol = div.find_element(By.TAG_NAME,"ol")
li = ol.find_elements(By.TAG_NAME,"li")
links = [li.find_element(By.TAG_NAME,"a").get_attribute('href') for li in li]

driver.quit()

pdfs = []

for link in links:
    nome_arquivo = link.split("/")[-1]
    resposta = requests.get (link, stream=True)
    pasta_pdf= os.path.join(pasta,nome_arquivo)
    with open (pasta_pdf,"wb") as arquivo:
        for chunk in resposta.iter_content(chunk_size=8192):
            arquivo.write(chunk)   
    pdfs.append(pasta_pdf)


nome="pdfs_mesclados.zip"
with zipfile.ZipFile (nome, 'w',zipfile.ZIP_DEFLATED) as zipf:
    for pdf_files in pdfs:
        zipf.write(pdf_files,os.path.basename(pdf_files))


