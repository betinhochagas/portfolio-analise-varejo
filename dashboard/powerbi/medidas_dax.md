# Medidas DAX — Painel de Vendas (Power BI)

Crie cada medida em **Modelagem → Nova medida** e cole o código.
A tabela importada se chama **`vendas_looker`** (nome do CSV).

> 💡 Depois de criar, selecione a medida e ajuste o **Formato** na faixa superior
> (Moeda R$ para valores, Porcentagem para margem).

---

## 1. Faturamento
```DAX
Faturamento = SUM(vendas_looker[valor_total])
```
Formato: **Moeda** → R$ Português (Brasil). Resultado esperado: **R$ 12.229.507,07**

## 2. Lucro
```DAX
Lucro = SUM(vendas_looker[lucro])
```
Formato: **Moeda** R$. Esperado: **R$ 4.810.714,97**

## 3. Nº de Vendas
```DAX
Nº de Vendas = COUNTROWS(vendas_looker)
```
Formato: **Número inteiro** (separador de milhar). Esperado: **12.000**

## 4. Ticket Médio
```DAX
Ticket Médio = DIVIDE([Faturamento], [Nº de Vendas])
```
Formato: **Moeda** R$. Esperado: **R$ 1.019,13**

## 5. Margem %
```DAX
Margem % = DIVIDE([Lucro], [Faturamento])
```
Formato: **Porcentagem** com 2 casas. Esperado: **39,34%**

---

### (Opcional) Medidas extras que impressionam
```DAX
-- Faturamento do mês anterior (para variação)
Faturamento Mês Anterior =
CALCULATE([Faturamento], DATEADD(vendas_looker[data_venda], -1, MONTH))

-- Variação % mês a mês
Var. % MoM =
DIVIDE([Faturamento] - [Faturamento Mês Anterior], [Faturamento Mês Anterior])
```
> Para essas duas funcionarem bem, marque `data_venda` como tipo **Data** e,
> idealmente, crie uma tabela de calendário. Deixe como evolução futura.
