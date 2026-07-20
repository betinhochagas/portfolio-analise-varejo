// Consulta Power Query (M) para importar vendas_looker.csv no Power BI.
// Cole no Editor Avancado (Power Query -> Pagina Inicial -> Editor Avancado),
// substituindo TODO o conteudo. Resolve o problema de decimal (ponto) no pt-BR
// usando o locale "en-US" na conversao das colunas numericas.
let
    // 1. Carrega o CSV (23 colunas, delimitador virgula, UTF-8)
    Fonte = Csv.Document(
        File.Contents("C:\Engenharia de Dados\portfolio-varejo\dados\tratado\vendas_looker.csv"),
        [Delimiter = ",", Columns = 23, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),

    // 2. Primeira linha vira cabecalho
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),

    // 3. Colunas de texto e inteiras (locale nao importa aqui)
    TiposBase = Table.TransformColumnTypes(Cabecalhos, {
        {"venda_id", Int64.Type},
        {"ano", Int64.Type},
        {"mes", Int64.Type},
        {"ano_mes", type text},
        {"trimestre", type text},
        {"dia_semana", type text},
        {"produto_id", Int64.Type},
        {"produto", type text},
        {"categoria", type text},
        {"quantidade", Int64.Type},
        {"regiao", type text},
        {"cidade", type text},
        {"canal", type text},
        {"forma_pagamento", type text},
        {"cliente_id", Int64.Type}
    }),

    // 4. Data + decimais convertidos USANDO LOCALE Ingles-EUA (ponto = decimal)
    TiposLocaleEUA = Table.TransformColumnTypes(TiposBase, {
        {"data_venda", type date},
        {"preco_unitario", type number},
        {"desconto", type number},
        {"custo_unitario", type number},
        {"custo_total", type number},
        {"valor_total", type number},
        {"lucro", type number},
        {"margem_pct", type number}
    }, "en-US")
in
    TiposLocaleEUA
