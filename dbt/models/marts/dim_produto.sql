-- Dimensao Produto: um registro por produto.
select distinct
    produto_id,
    produto,
    categoria
from {{ ref('stg_vendas') }}
