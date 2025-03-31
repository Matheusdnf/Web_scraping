# Como Utilizar o Projeto

Este repositório contém scripts Python organizados em 4 diretórios, cada um com uma tarefa específica. O projeto envolve **Web Scraping**, **Povoamento de Banco de Dados MySQL**, **Criação de API com FastAPI** e uma **Aplicação Web**.

## Instalando as Dependências

O projeto depende de algumas bibliotecas Python. Para instalar todas as dependências necessárias, basta usar o arquivo `requirements.txt`.

1. Clone o repositório ou baixe os arquivos do projeto.
2. Abra o terminal ou prompt de comando e navegue até a pasta do projeto.
3. Instale as dependências com o seguinte comando:
   ```bash
   pip install -r requirements.txt
   ```

## Estrutura do Projeto

### Task_1

- **O que faz**: Realiza **web scraping** e Baixa dois arquivos PDF do [site da ANS](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos) e compacta em **.zip**.

### Task_2

- **O que faz**: Realiza **web scraping** Baixa alguns arquivos CSV de um site e compacta em **.zip**.

### Task_3

- **O que faz**:
  - Scripts 3.1 e 3.2: Realizam **web scraping** e baixam arquivos **.zip**, descompactando-os.
  - Script `criar_banco`: Cria um banco de dados MySQL e popula com os dados extraídos.
  - Arquivos `.sql` com o esquema de banco e queries de consulta.

### Task_4

Para funcionar é necessários rodar ambos os códigos ao mesmo tempo.

- **O que faz**:
  1. **Server**: Possue um script em python e um arquivo **.csv** que será utilizado como conteúdo da api, e um arquivo em **.py** que Inicia um servidor local com FastAPI.
  2. Para Ele Funcionar Execute:
     ```bash
     python -m uvicorn server:app --reload
     ```
- **Pasta Matheus_diniz**: Uma Aplicação web que exibe os dados da API.

Na raiz do projeto, há uma coleção de requisições no **Postman** para testar a API.

---

## Ferramentas Utilizadas

- Python v3.12
- Visual Studio Code (IDE)
- Vue.js
- Postman
- MySQL
