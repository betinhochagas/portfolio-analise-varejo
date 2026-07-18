-- Dimensao Tempo: um registro por data de venda, com partes derivadas.
select distinct
    data_venda,
    extract(year  from data_venda)                       as ano,
    extract(month from data_venda)                        as mes,
    format_date('%Y-%m', data_venda)                      as ano_mes,
    'T' || cast(extract(quarter from data_venda) as string) as trimestre,
    format_date('%A', data_venda)                         as dia_semana
from {{ ref('stg_vendas') }}
