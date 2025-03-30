CREATE TABLE IF NOT EXISTS operadoras (
    registro_operadora VARCHAR(10) NOT NULL PRIMARY KEY ,
    cnpj             VARCHAR(14) NOT NULL,
    unique(cnpj);
    razao_social     VARCHAR(150),
    nome_fantasia    VARCHAR(150),
    modalidade       VARCHAR(100),
    logradouro       VARCHAR(100),
    numero           VARCHAR(20),
    complemento      VARCHAR(100),
    bairro           VARCHAR(50),
    cidade           VARCHAR(50),
    uf               VARCHAR(2),
    cep              VARCHAR(8),
    ddd              VARCHAR(4),
    telefone         VARCHAR(20),
    fax              VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante    VARCHAR(50),
    cargo_representante VARCHAR(40),
    regiao_de_comercializacao INT (1),
    data_registro_ANS DATE
);

CREATE TABLE demonstracoes_contabeis (
    data DATE,
    reg_ans BIGINT,
    cd_conta_contabil BIGINT ,
    descricao VARCHAR(150) 
    vl_saldo_inicial DECIMAL(15,2),
    vl_saldo_final DECIMAL(15,2) ,
    
    PRIMARY KEY (data, reg_ans, cd_conta_contabil),
) ;