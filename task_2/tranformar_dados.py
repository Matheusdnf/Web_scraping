import zipfile
import pdfplumber
import pandas as pd
import csv


#Necessita ter executado task_1 primeiro 
pdf_file = "./task_1/anexos_pdfs/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_output = "task_2/tabelas_extraidas.csv"
zip_output = "./task_2/Teste_{Matheus_Diniz}.zip"

todas_tabelas = []

#irá abrir o pdf e unir todas as tabelas
with pdfplumber.open(pdf_file) as pdf:
    for i, page in enumerate(pdf.pages):
        tabelas = page.extract_tables()
        for tabela in tabelas:
            df = pd.DataFrame(tabela)
            # Remove quebras de linha e espaços extras em cada célula
            df = df.applymap(lambda x: x.replace("\n", " ").strip() if isinstance(x, str) else x)
            df.replace({"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}, inplace=True)
            todas_tabelas.append(df)

# Junta todas as tabelas e salva em um único CSV
if todas_tabelas:
    df_final = pd.concat(todas_tabelas, ignore_index=True)
    df_final.to_csv(csv_output, index=False, header=False, encoding="utf-8-sig",
                    sep=";", quoting=csv.QUOTE_ALL)
    print(f"Tabelas extraídas e salvas em {csv_output}")
    
    # Cria um arquivo ZIP contendo o CSV
    with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_output)
    print(f"Arquivo ZIP criado: {zip_output}")
else:
    print("Nenhuma tabela encontrada no PDF.")
