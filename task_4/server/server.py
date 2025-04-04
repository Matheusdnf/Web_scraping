from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import logging
from fastapi import Query

#Digite esté comando -> python -m uvicorn server:app --reload 
#Assim o servidor será colocado no ar

#utilização de fast api para colocar o servidor no ar
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    csv_path =  "Relatorio_cadop.csv"
    logger.info(f"Tentando carregar CSV de: {csv_path}")
    
    df = pd.read_csv(
        csv_path,
        sep=';',
        encoding='utf-8',
        dtype=str,
        quotechar='"',
        on_bad_lines='skip'
    )
    
    df.columns = df.columns.str.strip().str.lower()

    
except Exception as e:
    logger.error(f"FALHA CRÍTICA: {str(e)}")
    df = pd.DataFrame()

#rota padrão retornando o estado da api e os endpoints
@app.get("/")
async def root():
    return {
        "message": "API de Operadoras ANS",
        "endpoints": {
            "busca": "/buscar/{termo}",
            "detalhes": "/operadora/{registro_ans}",
            "todos_dados": "/todos-dados",
            "status": "OK", "csv_loaded": not df.empty
        }
    }

#busca por qualquer termo que exista no csv
@app.get("/buscar/{termo}")
async def buscar(termo: str, limite: int = 5):
    if df.empty:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    try:
        mask = df.apply(lambda col: col.astype(str).str.contains(termo, case=False)).any(axis=1)
        print(mask)
        resultados = df[mask].head(limite)
        print(resultados)
        
        return {
            "termo": termo,
            "resultados": resultados.fillna("").to_dict(orient='records')
        }
    
    except Exception as e:
        logger.error(f"Erro na busca: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno")

# busca pelo nome fantasia da empresa
@app.get("/nome_fantasia/{nome_fantasia}") 
async def detalhes(nome_fantasia: str):
    if df.empty:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    operadoras = df[df['nome_fantasia'].astype(str).str.upper() == nome_fantasia.upper()]
    
    if operadoras.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma operadora encontrada na UF: {nome_fantasia}"
        )

    return operadoras.fillna("").to_dict(orient='records')

# endpoint que retorna tudo que estiver no csv
@app.get("/tudo")
async def todos_dados(
    aumentar_quantidade: int = Query(None, description="Quantidade adicional de itens para carregar"),
    limite: int = Query(None, description="Limite máximo inicial de registros"),
    pagina: int = Query(1, description="Número da página atual"),
    itens_por_pagina: int = Query(10, description="Itens exibidos por página")
):
    if df.empty:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    try:

        if aumentar_quantidade:
            if limite:
                novo_limite = limite + aumentar_quantidade
            else:
                novo_limite = (pagina * itens_por_pagina) + aumentar_quantidade
            
            dados = df.head(novo_limite)

        elif limite:
            dados = df.head(limite)
        else:
            inicio = (pagina - 1) * itens_por_pagina
            fim = inicio + itens_por_pagina
            dados = df.iloc[inicio:fim]
        
        return {
            "total_registros": len(df),
            "parametros_usados": {
                "limite": limite,
                "pagina": pagina,
                "itens_por_pagina": itens_por_pagina,
                "aumentar_quantidade": aumentar_quantidade
            },
            "registros_retornados": len(dados),
            "dados": dados.fillna("").to_dict(orient='records')
        }
    
    except Exception as e:
        logger.error(f"Erro ao recuperar dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno")