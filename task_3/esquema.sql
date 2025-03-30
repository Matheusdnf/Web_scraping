CREATE TABLE IF NOT EXISTS operadoras (
    registro_operadora VARCHAR(6) PRIMARY KEY,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    razao_social VARCHAR(140),
    nome_fantasia VARCHAR(140),
    modalidade VARCHAR(255),
    logradouro VARCHAR(40),
    numero VARCHAR(20),
    complemento VARCHAR(40),
    bairro VARCHAR(30),
    cidade VARCHAR(30),
    uf VARCHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(4),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(50),
    cargo_representante VARCHAR(40),
    regiao_de_comercializacao INT CHECK (regiao_de_comercializacao BETWEEN 1 AND 6),
    data_registro_ans DATE
);

CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    data DATE NOT NULL,
    registro_operadora VARCHAR(6) NOT NULL, 
    cd_conta_contabil BIGINT NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    vl_saldo_inicial DECIMAL(15,2),
    vl_saldo_final DECIMAL(15,2),
    PRIMARY KEY (data, registro_operadora, cd_conta_contabil),
    FOREIGN KEY (registro_operadora) REFERENCES operadoras(registro_operadora)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);