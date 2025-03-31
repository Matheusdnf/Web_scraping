import os
def criar_pasta(nome_da_pasta):
    try:
        if os.path.exists(nome_da_pasta):
            print(f"Já existe uma pasta com o nome {nome_da_pasta}")
        else:
            os.mkdir(nome_da_pasta)
    except OSError:
        print("Não foi possível criar um arquivo")
