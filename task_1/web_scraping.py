import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import zipfile
import os
import sys
#criação de uma biblioteca de funções genericas
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from funcoes.funcoes_genereicas import criar_pasta


driver = webdriver.Chrome()
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
driver.get(url)

div = driver.find_element(By.CLASS_NAME,"cover-richtext-tile.tile-content")

ol = div.find_element(By.TAG_NAME,"ol")
lis = ol.find_elements(By.TAG_NAME,"li")


links=[]

for li in lis:
    a_tag = li.find_element(By.TAG_NAME,"a")
    link= a_tag.get_attribute('href')
    links.append(link)


driver.quit()

pdfs = []

pasta_pdf="./task_1/anexos_pdfs"

criar_pasta(pasta_pdf)

# baixar os pdfs
for i,link in enumerate(links):
    nome_arquivo = link.split("/")[-1]
    resposta = requests.get (link, stream=True)
    caminho_arquivo = os.path.join(pasta_pdf, nome_arquivo)
    print(f"Baixando o {i+1}° pdf...")
    with open (caminho_arquivo,"wb") as arquivo:
        for chunk in resposta.iter_content(chunk_size=8192):
            arquivo.write(chunk)   
    pdfs.append(pasta_pdf)
print("Pdf Baixados Com sucesso.")

# Compactar em formato zip
nome="./task_1/anexos_pdfs_mesclados.zip"
with zipfile.ZipFile (nome, 'w',zipfile.ZIP_DEFLATED) as zipf:
    for pdf_files in pdfs:
        zipf.write(pdf_files,os.path.basename(pdf_files))


