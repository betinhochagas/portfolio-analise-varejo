-- Dimensao Local: um registro por combinacao regiao + cidade.
-- Usa chave substituta (surrogate key) gerada com dbt_utils.
select distinct
    {{ dbt_utils.generate_surrogate_key(['regiao', 'cidade']) }} as local_sk,
    regiao,
    cidade
from {{ ref('stg_vendas') }}
