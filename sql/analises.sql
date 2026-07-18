-- ===========================================================================
-- analises.sql  |  Analise de Vendas de Varejo (modelo estrela - SQLite)
-- ---------------------------------------------------------------------------
-- Banco: dados/tratado/varejo.db
-- Tabelas:
--   fato_vendas (venda_id, data_venda, produto_id, local_id, cliente_id,
--                quantidade, preco_unitario, desconto, custo_total,
--                valor_total, lucro, canal, forma_pagamento)
--   dim_produto (produto_id, produto, categoria, custo_unitario, preco_unitario)
--   dim_local   (local_id, regiao, cidade)
--   dim_tempo   (data_venda, ano, mes, ano_mes, trimestre, dia_semana)
--
-- Cada consulta responde a uma pergunta de negocio.
-- ===========================================================================


-- ---------------------------------------------------------------------------
-- 1) VISAO GERAL: KPIs principais do periodo
-- ---------------------------------------------------------------------------
SELECT
    COUNT(*)                         AS total_vendas,
    SUM(quantidade)                  AS itens_vendidos,
    ROUND(SUM(valor_total), 2)       AS faturamento,
    ROUND(SUM(lucro), 2)             AS lucro_total,
    ROUND(AVG(valor_total), 2)       AS ticket_medio,
    ROUND(SUM(lucro) * 100.0 / SUM(valor_total), 1) AS margem_media_pct
FROM fato_vendas;


-- ---------------------------------------------------------------------------
-- 2) Faturamento e lucro por CATEGORIA (JOIN fato + dim_produto)
-- ---------------------------------------------------------------------------
SELECT
    p.categoria,
    COUNT(*)                         AS vendas,
    ROUND(SUM(f.valor_total), 2)     AS faturamento,
    ROUND(SUM(f.lucro), 2)           AS lucro,
    ROUND(SUM(f.lucro) * 100.0 / SUM(f.valor_total), 1) AS margem_pct
FROM fato_vendas f
JOIN dim_produto p ON f.produto_id = p.produto_id
GROUP BY p.categoria
ORDER BY faturamento DESC;


-- ---------------------------------------------------------------------------
-- 3) TOP 10 produtos por faturamento
-- ---------------------------------------------------------------------------
SELECT
    p.produto,
    p.categoria,
    SUM(f.quantidade)                AS itens,
    ROUND(SUM(f.valor_total), 2)     AS faturamento
FROM fato_vendas f
JOIN dim_produto p ON f.produto_id = p.produto_id
GROUP BY p.produto, p.categoria
ORDER BY faturamento DESC
LIMIT 10;


-- ---------------------------------------------------------------------------
-- 4) Faturamento por REGIAO e participacao (%) sobre o total
--    -> usa window function SUM() OVER () para calcular o % do todo
-- ---------------------------------------------------------------------------
SELECT
    l.regiao,
    ROUND(SUM(f.valor_total), 2)     AS faturamento,
    ROUND(
        SUM(f.valor_total) * 100.0 / SUM(SUM(f.valor_total)) OVER (),
        1
    )                                AS participacao_pct
FROM fato_vendas f
JOIN dim_local l ON f.local_id = l.local_id
GROUP BY l.regiao
ORDER BY faturamento DESC;


-- ---------------------------------------------------------------------------
-- 5) EVOLUCAO MENSAL do faturamento + crescimento vs mes anterior
--    -> window function LAG() para comparar com o mes anterior
-- ---------------------------------------------------------------------------
WITH mensal AS (
    SELECT
        t.ano_mes,
        ROUND(SUM(f.valor_total), 2) AS faturamento
    FROM fato_vendas f
    JOIN dim_tempo t ON f.data_venda = t.data_venda
    GROUP BY t.ano_mes
)
SELECT
    ano_mes,
    faturamento,
    LAG(faturamento) OVER (ORDER BY ano_mes) AS mes_anterior,
    ROUND(
        (faturamento - LAG(faturamento) OVER (ORDER BY ano_mes))
        * 100.0 / LAG(faturamento) OVER (ORDER BY ano_mes),
        1
    )                                AS crescimento_pct
FROM mensal
ORDER BY ano_mes;


-- ---------------------------------------------------------------------------
-- 6) RANKING de produtos DENTRO de cada categoria
--    -> window function RANK() particionada por categoria
-- ---------------------------------------------------------------------------
WITH ranking AS (
    SELECT
        p.categoria,
        p.produto,
        ROUND(SUM(f.valor_total), 2) AS faturamento,
        RANK() OVER (
            PARTITION BY p.categoria
            ORDER BY SUM(f.valor_total) DESC
        )                            AS posicao
    FROM fato_vendas f
    JOIN dim_produto p ON f.produto_id = p.produto_id
    GROUP BY p.categoria, p.produto
)
SELECT categoria, posicao, produto, faturamento
FROM ranking
WHERE posicao <= 3          -- top 3 de cada categoria
ORDER BY categoria, posicao;


-- ---------------------------------------------------------------------------
-- 7) Desempenho por CANAL de venda
-- ---------------------------------------------------------------------------
SELECT
    canal,
    COUNT(*)                         AS vendas,
    ROUND(SUM(valor_total), 2)       AS faturamento,
    ROUND(AVG(valor_total), 2)       AS ticket_medio
FROM fato_vendas
GROUP BY canal
ORDER BY faturamento DESC;


-- ---------------------------------------------------------------------------
-- 8) TOP 10 clientes por valor gasto (clientes mais valiosos)
-- ---------------------------------------------------------------------------
SELECT
    cliente_id,
    COUNT(*)                         AS compras,
    ROUND(SUM(valor_total), 2)       AS total_gasto,
    ROUND(AVG(valor_total), 2)       AS ticket_medio
FROM fato_vendas
GROUP BY cliente_id
ORDER BY total_gasto DESC
LIMIT 10;


-- ---------------------------------------------------------------------------
-- 9) Faturamento por dia da semana (quando se vende mais?)
-- ---------------------------------------------------------------------------
SELECT
    t.dia_semana,
    COUNT(*)                         AS vendas,
    ROUND(SUM(f.valor_total), 2)     AS faturamento
FROM fato_vendas f
JOIN dim_tempo t ON f.data_venda = t.data_venda
GROUP BY t.dia_semana
ORDER BY faturamento DESC;


-- ---------------------------------------------------------------------------
-- 10) Impacto do DESCONTO no faturamento e na margem
-- ---------------------------------------------------------------------------
SELECT
    CASE
        WHEN desconto = 0    THEN 'Sem desconto'
        WHEN desconto <= 0.10 THEN 'Ate 10%'
        ELSE 'Acima de 10%'
    END                              AS faixa_desconto,
    COUNT(*)                         AS vendas,
    ROUND(SUM(valor_total), 2)       AS faturamento,
    ROUND(SUM(lucro) * 100.0 / SUM(valor_total), 1) AS margem_pct
FROM fato_vendas
GROUP BY faixa_desconto
ORDER BY faturamento DESC;
