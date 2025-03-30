use operadoras;
SELECT 
    o.razao_social AS "Razão Social",
    o.nome_fantasia AS "Nome Fantasia",
    FORMAT(SUM(d.vl_saldo_final - d.vl_saldo_inicial), 2, 'pt_BR') AS "Despesa Trimestral (R$)"
FROM 
    demonstracoes_contabeis d
JOIN 
    operadoras o ON d.registro_operadora = o.registro_operadora
WHERE 
    d.descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.data = (SELECT MAX(data) FROM demonstracoes_contabeis)
    AND o.razao_social IS NOT NULL  
    AND o.nome_fantasia IS NOT NULL 
GROUP BY 
    o.registro_operadora, o.razao_social, o.nome_fantasia, d.data
ORDER BY 
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) DESC
LIMIT 10;

SELECT
    o.razao_social AS "Razão Social",
    o.nome_fantasia AS "Nome Fantasia",
    FORMAT(SUM(d.vl_saldo_final - d.vl_saldo_inicial), 2, 'pt_BR') AS "Despesa Anual (R$)",
    CONCAT(
        DATE_FORMAT(DATE_SUB(last_date, INTERVAL 1 YEAR), '%b/%Y'),
        ' a ',
        DATE_FORMAT(last_date, '%b/%Y')
    ) AS "Período"
FROM
    demonstracoes_contabeis d
JOIN
    operadoras o ON d.registro_operadora = o.registro_operadora
CROSS JOIN
    (SELECT MAX(data) AS last_date FROM demonstracoes_contabeis) AS md
WHERE
    d.descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND d.data BETWEEN
        DATE_SUB(md.last_date, INTERVAL 1 YEAR)
        AND md.last_date
    AND o.razao_social IS NOT NULL
    AND o.nome_fantasia IS NOT NULL
GROUP BY
    o.registro_operadora, o.razao_social, o.nome_fantasia, md.last_date
ORDER BY
    SUM(d.vl_saldo_final - d.vl_saldo_inicial) DESC
LIMIT 10;