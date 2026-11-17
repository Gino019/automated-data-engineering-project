# Video script — 4 minutes 20 seconds (English)

**00:00–00:25 — Introduction**

“Hello! Today I am presenting FlowForge DE, an open-source data engineering pipeline using Python, dbt, DuckDB, and GitHub Actions. It transforms raw source files into tested analytical datasets and a public web dashboard, without AWS.”

**00:25–00:55 — Architecture**

“Python creates synthetic orders, customers, and products. DuckDB loads raw data, while dbt structures transformations into staging, fact, and analytical mart layers. The output is aggregated JSON consumed by GitHub Pages.”

**00:55–01:35 — Ingestion**

“The project generates 3,200 orders, 260 customers, and 48 products. Orders can be completed, cancelled, or refunded. The pipeline ensures that non-completed transactions do not count as revenue.”

**01:35–02:18 — dbt transformations**

“dbt standardizes field names and types, joins source dimensions, computes revenue, costs, and profit, and aggregates results by month, category, and region. Data tests validate required fields, unique IDs, allowed statuses, and referential integrity.”

**02:18–02:55 — CI/CD**

“GitHub Actions automates extraction, loading, transformation, testing, export, and deployment. It runs on code pushes, a manual trigger, and a daily schedule. A failed quality gate blocks publication.”

**02:55–03:38 — Dashboard**

“The public dashboard shows revenue, completed orders, profit, margin, trends, categories, and regional insights. Filters let users explore data, and only aggregates are published.”

**03:38–04:20 — Conclusion**

“The result is a reproducible data engineering case study with open-source tools and cloud publication without AWS. The repository and the English article are linked in the description. Thank you!”

**Note:** Verify the live site and CI execution before claiming the deployment succeeded. The dataset is entirely synthetic.
