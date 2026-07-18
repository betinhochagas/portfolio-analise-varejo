-- Staging: limpeza leve e selecao de colunas, 1:1 com a fonte raw.
-- Aqui NAO se agrega nem se junta nada — so padroniza para as marts.

with fonte as (
    select * from {{ source('varejo_raw', 'raw_vendas') }}
)

select
    -- chaves
    venda_id,
    produto_id,
    cliente_id,

    -- data (as partes de tempo sao derivadas na dim_tempo)
    data_venda,

    -- atributos de produto
    produto,
    categoria,

    -- atributos de local
    regiao,
    cidade,

    -- atributos de transacao (dimensoes degeneradas)
    canal,
    forma_pagamento,

    -- medidas
    quantidade,
    preco_unitario,
    desconto,
    custo_unitario,
    custo_total,
    valor_total,
    lucro,
    margem_pct

from fonte
