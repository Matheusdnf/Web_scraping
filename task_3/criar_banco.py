import csv
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

def verificar_tabelas(conexao):
    cursor = conexao.cursor()
    try:
        # Verifica se a tabela de operadoras existe
        cursor.execute("SHOW TABLES LIKE 'operadoras'")
        if not cursor.fetchone():
            raise Exception("Tabela 'operadoras' não existe")
            
        # Verifica se a tabela de demonstrações existe
        cursor.execute("SHOW TABLES LIKE 'demonstracoes_contabeis'")
        if not cursor.fetchone():
            raise Exception("Tabela 'demonstracoes_contabeis' não existe")
            
    finally:
        cursor.close()

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
    if value is None or value.strip() == '':
        return None
    value = value.strip()
    # Substitui vírgula por ponto para decimais
    if isinstance(value, str) and ',' in value:
        value = value.replace('.', '').replace(',', '.')  # Remove pontos de milhar e converte vírgula
    return value

def importar_dados_csv(conexao, arquivo_csv):
    try:
        cursor = conexao.cursor()

        # Desativa temporariamente a verificação de chaves estrangeiras
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        with open(arquivo_csv, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=';')
            
            for row in csvreader:
                registro_operadora = clean_value(row['Registro_ANS'])[:6]  # Garante máximo 6 caracteres
                
                try:
                    # Converte região de comercialização para inteiro ou NULL
                    regiao = clean_value(row['Regiao_de_Comercializacao'])
                    regiao_comercializacao = int(regiao) if regiao and regiao.isdigit() else None
                    
                    cursor.execute('''
                    INSERT INTO operadoras VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ''', (
                        registro_operadora, 
                        clean_value(row['CNPJ']),
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
                        clean_value(row['Telefone']),
                        clean_value(row['Fax']),
                        clean_value(row['Endereco_eletronico']),
                        clean_value(row['Representante']),
                        clean_value(row['Cargo_Representante']),
                        regiao_comercializacao,  # Já tratado como inteiro ou NULL
                        clean_date(row['Data_Registro_ANS'])
                    ))
                except Error as e:
                    print(f"Erro ao inserir operadora {registro_operadora}: {e}")
                    continue

        conexao.commit()
        print("Dados das operadoras importados com sucesso!")
    except Error as e:
        print(f"Erro ao importar dados CSV: {e}")
        conexao.rollback()
    finally:
        # Reativa a verificação de chaves estrangeiras
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        if cursor:
            cursor.close()



def clean_date(date_str):
    if not date_str or str(date_str).strip() == '':
        return None
    
    date_str = str(date_str).strip()
    
    try:
        # Tenta parsear como DD/MM/YYYY
        if '/' in date_str:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y-%m-%d')
        
        # Tenta parsear como YYYY-MM-DD (já está no formato correto)
        elif '-' in date_str:
            datetime.strptime(date_str, '%Y-%m-%d')  # Apenas valida
            return date_str
            
    except ValueError as e:
        print(f"Formato de data inválido: {date_str} - {e}")
        return None
    
    return None

def importar_demonstracoes_csv(conexao, caminho_pasta):
    try:
        cursor = conexao.cursor()
        arquivos_processados = 0
        registros_importados = 0
        erros = 0

        # Primeiro verifica quais operadoras existem
        cursor.execute("SELECT registro_operadora FROM operadoras")
        operadoras_validas = {row[0] for row in cursor.fetchall()}

        # Desativa temporariamente a verificação de chaves estrangeiras
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        for arquivo in os.listdir(caminho_pasta):
            if arquivo.lower().endswith('.csv'):
                caminho_completo = os.path.join(caminho_pasta, arquivo)
                print(f"\nProcessando arquivo: {arquivo}")
                
                try:
                    with open(caminho_completo, 'r', encoding='utf-8') as csvfile:
                        csvreader = csv.DictReader(csvfile, delimiter=';')
                        
                        for row in csvreader:
                            registro_op = clean_value(row['REG_ANS'])[:6]  # Garante máximo 6 caracteres
                            
                            # Verifica se a operadora existe antes de inserir
                            if registro_op not in operadoras_validas:
                                print(f"Operadora {registro_op} não encontrada - registro ignorado")
                                erros += 1
                                continue
                            
                            try:
                                cursor.execute('''
                                INSERT INTO demonstracoes_contabeis 
                                (data, registro_operadora, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) 
                                VALUES (%s, %s, %s, %s, %s, %s)
                                ''', (
                                    clean_date(row['DATA']),
                                    registro_op,
                                    clean_value(row['CD_CONTA_CONTABIL']),
                                    clean_value(row['DESCRICAO']),
                                    clean_value(row['VL_SALDO_INICIAL']),
                                    clean_value(row['VL_SALDO_FINAL'])
                                ))
                                registros_importados += 1
                            except Error as e:
                                erros += 1
                                print(f"Erro ao inserir registro: {e}")
                                continue
                    
                    arquivos_processados += 1
                    print(f"Arquivo {arquivo} processado com sucesso!")
                    
                except Exception as e:
                    print(f"Erro ao processar arquivo {arquivo}: {e}")
                    continue

        conexao.commit()
        print(f"\nResumo da importação:")
        print(f"- Arquivos processados: {arquivos_processados}")
        print(f"- Registros importados: {registros_importados}")
        print(f"- Erros encontrados: {erros}")
        
    except Error as e:
        print(f"Erro durante a importação: {e}")
        conexao.rollback()
    finally:
        # Reativa a verificação de chaves estrangeiras
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
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

    
    executar_script_sql("./task_3/esquema.sql", conn)

    verificar_tabelas(conn)

    importar_dados_csv(conn, './task_3/pasta_csv/Relatorio_cadop.csv')
    
    importar_demonstracoes_csv(conn,"./task_3/arquivos_descompactados")
    

except Error as e:
    print(f"Erro no processo principal: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():  # Verifica se existe e está aberta
        conn.close()
        print("Conexão encerrada.")