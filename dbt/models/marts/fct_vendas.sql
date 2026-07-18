-- Fato Vendas: grao = uma linha por venda_id.
-- Chaves estrangeiras para as dimensoes + medidas + dimensoes degeneradas.
with v as (
    select * from {{ ref('stg_vendas') }}
)

select
    -- chave do fato
    v.venda_id,

    -- chaves estrangeiras (FK) para as dimensoes
    v.produto_id,
    {{ dbt_utils.generate_surrogate_key(['v.regiao', 'v.cidade']) }} as local_sk,
    v.data_venda,

    -- dimensoes degeneradas
    v.cliente_id,
    v.canal,
    v.forma_pagamento,

    -- medidas
    v.quantidade,
    v.preco_unitario,
    v.desconto,
    v.custo_total,
    v.valor_total,
    v.lucro,
    v.margem_pct

from v
