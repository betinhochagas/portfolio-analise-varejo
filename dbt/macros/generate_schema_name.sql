{#-
  Override do dbt: por padrao o dbt PREFIXA o schema custom com o schema do
  target (ex.: "varejo_dbt_varejo_marts"). Este override usa o nome custom
  como esta, gerando datasets limpos: "varejo_staging" e "varejo_marts".
-#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
