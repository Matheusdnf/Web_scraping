import csv
import mysql.connector
from mysql.connector import Error

def criar_banco_se_nao_existir(conexao, nome_banco):
    try:
        cursor = conexao.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nome_banco}")
        cursor.execute(f"USE {nome_banco}")
        print(f"Banco de dados '{nome_banco}' verificado/criado com sucesso!")
    except Error as e:
        print(f"Erro ao criar banco de dados: {e}")
    finally:
        if cursor:
            cursor.close()

def executar_script_sql(arquivo_sql, conexao):
    try:
        cursor = conexao.cursor()
        
        with open(arquivo_sql, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conexao.commit()
        print("Script SQL executado com sucesso!")
    except Error as e:
        print(f"Erro ao executar script SQL: {e}")
    finally:
        if cursor:
            cursor.close()
def clean_value(value):
    return None if value is None or value.strip() == '' else value.strip()

def importar_dados_csv(conexao, arquivo_csv):
    try:
        cursor = conexao.cursor()

        with open(arquivo_csv, 'r', encoding='utf-8') as csvfile:
            # Usa DictReader com delimitador correto e cabeçalho na primeira linha
            csvreader = csv.DictReader(csvfile, delimiter=';')
            
            for row in csvreader:
                registro_operadora = clean_value(row['Registro_ANS'])

                
                
                try:
                    cursor.execute('''
                    INSERT INTO operadoras VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        registro_operadora, 
                        row["CNPJ"],
                        clean_value(row['Razao_Social']),
                        clean_value(row['Nome_Fantasia']),
                        clean_value(row['Modalidade']),
                        clean_value(row['Logradouro']),
                        clean_value(row['Numero']),
                        clean_value(row['Complemento']),
                        clean_value(row['Bairro']),
                        clean_value(row['Cidade']),
                        clean_value(row['UF']),
                        clean_value(row['CEP']),
                        clean_value(row['DDD']),
                        clean_value(row['Telefone'])
                    ))
                except Error as e:
                    print(f"Erro ao inserir registro {registro_operadora}: {e}")
                    continue

        conexao.commit()
        print("Dados CSV importados com sucesso!")
    except Error as e:
        print(f"Erro ao importar dados CSV: {e}")
        conexao.rollback()
    finally:
        if cursor:
            cursor.close()

try:
    nome_banco = "operadoras"
    
    # 1. Criar banco (com conexão root)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="senha"
    )
    criar_banco_se_nao_existir(conn, nome_banco)

    
    # 3. Executar script SQL e importar dados
    executar_script_sql('esquema.sql', conn)
    importar_dados_csv(conn, 'r.csv')

except Error as e:
    print(f"Erro no processo principal: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():  # Verifica se existe e está aberta
        conn.close()
        print("Conexão encerrada.")