# From Raw CSV to Cloud Dashboard: Building an Automated Data Engineering Pipeline with dbt, DuckDB and GitHub Actions

**A practical, open-source data engineering project featuring reproducible ingestion, SQL transformations, data quality checks, scheduled orchestration, and a public web dashboard — without AWS.**

**Author:** [Add your name]

**Repository:** [github.com/Gino019/automated-data-engineering-project](https://github.com/Gino019/automated-data-engineering-project)

**Live dashboard:** [gino019.github.io/automated-data-engineering-project/](https://gino019.github.io/automated-data-engineering-project/) — *confirm that GitHub Pages is deployed successfully before describing this as live.*

**Suggested tags:** Data Engineering, dbt, DuckDB, GitHub Actions, Python

**[FIGURE 1 — INSERT IMAGE `docs/images/01-cover.png` HERE]**

*Figure 1. FlowForge DE: a Python, dbt, DuckDB, and GitHub Actions data engineering case study. Conceptual illustration.*

## 1. Introduction: Why Data Engineering Matters

Business dashboards are only as reliable as the data behind them. Source files may contain inconsistent types, missing values, duplicate identifiers, invalid relationships, or records that must be excluded from financial calculations. A chart alone does not solve these problems. Data engineering addresses them by creating pipelines that transform raw sources into trustworthy, well-documented datasets.

This article explains **FlowForge DE**, a small but complete reproducible data engineering solution. It extracts synthetic e-commerce orders, customers, and products; ingests those records into DuckDB; uses dbt to build validated analytical models; and publishes an interactive dashboard. GitHub Actions automatically orchestrates the process on code pushes, manual workflow dispatches, and a daily schedule. No AWS account or paid database is required.

**[FIGURE 2 — INSERT `docs/images/02-architecture.png` HERE]**

*Figure 2. FlowForge DE reference architecture. The pipeline transforms CSV extracts into a public aggregate dataset.*

## 2. Project Objectives

The solution has five main objectives:

1. Automate the **extraction and ingestion** of reproducible source data.
2. Apply reliable, maintainable **SQL transformations** through dbt.
3. Enforce **data quality** through tests and validation gates.
4. Schedule and automate the pipeline with **GitHub Actions CI/CD**.
5. Publish analytics as a static public website without a running application server.

The output is not only a dashboard. It is a traceable process, from generated source files to tested published metrics.

## 3. Technology Stack

| Technology | Responsibility |
|---|---|
| Python | Synthetic source generation and CSV ingestion |
| DuckDB | Embedded analytical database / warehouse |
| dbt Core with dbt-duckdb | SQL transformations, data model dependencies, and tests |
| pytest | Checks for deterministic and internally consistent inputs |
| GitHub Actions | Pipeline orchestration and scheduled CI/CD runs |
| GitHub Pages | Public, static dashboard hosting |
| Chart.js | Interactive revenue trends and distributions |

DuckDB is an embedded columnar analytics database. In this design, the database file exists only during the automated build. The public application receives **aggregated JSON**, not a database connection or raw personal records. All customer data in the demonstration are synthetic.

## 4. Source Data and Extraction

Our sample data represents an e-commerce operation with three CSV source tables:

| Source | Example fields | Generated rows |
|---|---|---:|
| `orders.csv` | order_id, order_ts, customer_id, product_id, quantity, unit_price, status | 3,200 |
| `customers.csv` | customer_id, region, segment | 260 |
| `products.csv` | product_id, product_name, category, unit_cost, list_price | 48 |

The script `scripts/generate_data.py` uses a fixed random seed so the same inputs produce the same results. This makes errors repeatable and tests consistent. The order statuses include `completed`, `cancelled`, and `refunded`. Only completed orders appear in financial metrics.

```python
# Simplified excerpt from scripts/generate_data.py
rng = random.Random(2026)
status = rng.choices(
    ['completed', 'cancelled', 'refunded'],
    weights=[.88, .08, .04]
)[0]
```

For ingestion, `scripts/ingest.py` loads each CSV directly into DuckDB's `raw` schema:

```python
con.execute('CREATE SCHEMA IF NOT EXISTS raw')
con.execute(
    'CREATE OR REPLACE TABLE raw.orders AS '
    'SELECT * FROM read_csv_auto(?, HEADER=TRUE)',
    ['data/raw/orders.csv']
)
```

This separates **source extraction** from **warehouse loading**, making the workflow easier to audit and extend.

## 5. Building a dbt Transformation Layer

We use three modeling layers:

- **Raw:** ingested orders, customers, and products.
- **Staging:** typed and standardized source fields.
- **Marts:** a fact table of completed orders and a summarized sales cube.

**[FIGURE 3 — INSERT `docs/images/03-dbt-lineage.png` HERE]**

*Figure 3. dbt lineage concept: raw data, staging models, curated facts, and aggregated marts.*

The staging model cleans and standardizes source order fields:

```sql
-- models/staging/stg_orders.sql
select
    cast(order_id as integer) as order_id,
    cast(order_ts as timestamp) as order_ts,
    cast(customer_id as integer) as customer_id,
    cast(product_id as integer) as product_id,
    cast(quantity as integer) as quantity,
    cast(unit_price as decimal(12, 2)) as unit_price,
    lower(trim(status)) as order_status
from {{ source('raw', 'orders') }}
```

In the fact layer, transactions connect to the relevant customer and product dimensions. We calculate revenue, cost, and profit while excluding cancelled or refunded orders:

```sql
-- Core logic from models/marts/fct_completed_orders.sql
select
    o.order_id,
    c.region,
    p.category,
    round(o.quantity * o.unit_price, 2) as revenue,
    round(o.quantity * p.unit_cost, 2) as cost,
    round(o.quantity * (o.unit_price - p.unit_cost), 2) as profit
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c
  on o.customer_id = c.customer_id
join {{ ref('stg_products') }} p
  on o.product_id = p.product_id
where o.order_status = 'completed'
```

The curated `mart_sales_cube` then groups completed sales by month, region and category. Its output is compact enough to serve as static JSON.

## 6. Data Quality: Tests Before Publishing

A pipeline should fail if its inputs or output violate defined assumptions. The project combines two layers of quality control:

**Python tests** verify reproducible generation, valid dimension references, known order statuses, and consistency of the preview metrics.

**dbt data tests** verify unique keys, required fields, valid order status values, and relationships between orders and dimensions. A singular SQL test catches negative revenue or product cost, and the export script reconciles completed order counts against the final mart.

**[FIGURE 4 — INSERT `docs/images/06-data-quality.png` HERE]**

*Figure 4. Validation checks protecting FlowForge DE from inconsistent or invalid data. Diagram, not a test-run screenshot.*

A representative dbt data test is declared in YAML:

```yaml
columns:
  - name: order_id
    data_tests: [not_null, unique]
```

All transformations and tests are executed with:

```bash
dbt build --profiles-dir . --project-dir .
```

If an essential dbt test fails, the GitHub Actions pipeline stops before the public dashboard deployment. This protects published metrics from known failures.

## 7. Exporting a Public Analytics Dataset

A public static dashboard cannot query a temporary CI database directly. Instead, the pipeline exports a curated JSON file to `site/data/metrics.json`. The result is limited to aggregated fields:

```json
{
  "month": "2026-03",
  "year": 2026,
  "region": "West",
  "category": "Electronics",
  "orders": 15,
  "units": 37,
  "revenue": 9048.20,
  "profit": 2910.45
}
```

*The numbers above are an illustrative row format, not a verified query result.*

The dashboard renders revenue, order count, profit, margin, monthly trend, category split, regional share and a downloadable curated CSV. It includes region/year filters and displays pipeline provenance information, including the GitHub run ID when available.

**[FIGURE 5 — INSERT `docs/images/04-dashboard-preview.png` HERE]**

*Figure 5. FlowForge DE dashboard preview using synthetic, locally generated aggregate values. Published figures are replaced with verified dbt output when CI succeeds.*

The complete source for the dashboard is available in [`site/`](https://github.com/Gino019/automated-data-engineering-project/tree/main/site).

## 8. Automating and Scheduling with GitHub Actions

The key deployment component is the workflow in `.github/workflows/pipeline.yml`. It runs on every push to `main`, via manual dispatch, and on a scheduled daily UTC trigger.

```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: '23 7 * * *'
```

The principal job follows this sequence:

```bash
python -m pytest tests -q
python scripts/generate_data.py
python scripts/ingest.py
dbt build --profiles-dir . --project-dir .
python scripts/export_dashboard.py
python scripts/validate_artifact.py
```

Once the checks succeed, GitHub Actions uploads the `site/` directory as a Pages artifact. A separate deployment job publishes it on GitHub Pages. The workflow also stores the dbt manifest and run results as an auditable artifact. GitHub's scheduled workflow execution is best-effort and may be delayed.

**[FIGURE 6 — INSERT `docs/images/05-ci-workflow-illustration.png` HERE]**

*Figure 6. Example CI/CD workflow stages. This is a diagram, not proof of a successful deployment.*

To configure the website: open the repository's **Settings → Pages → Build and deployment** and select **GitHub Actions**. Then use the Actions tab to inspect the job results. A green workflow, not a conceptual illustration, is the evidence that the code has passed CI and deployed.

## 9. Running the Project Yourself

Clone the public repository and follow these commands (Python 3.11 recommended):

```bash
git clone https://github.com/Gino019/automated-data-engineering-project.git
cd automated-data-engineering-project
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
python -m pytest tests -q
python scripts/generate_data.py
python scripts/ingest.py
dbt build --profiles-dir . --project-dir .
python scripts/export_dashboard.py
python scripts/validate_artifact.py
python -m http.server 8080 --directory site
```

Open `http://localhost:8080` to inspect the dashboard. The GitHub Actions workflow performs the same transformation and validation sequence automatically. You can also run `python -m scripts.bootstrap_preview` to generate a **non-dbt preview** when dependencies are unavailable; this preview is clearly identified and is not substitute evidence for a real pipeline run.

## 10. Results, Limitations and Lessons Learned

The deterministic demonstration generator produces **3,200 synthetic orders, 260 customer records and 48 products**. A local Python preview produces **2,818 completed orders**, excluding 382 cancelled or refunded transactions; these results are reproducible for the fixed seed but must be confirmed against the actual dbt pipeline output once deployed.

This exercise demonstrates several useful engineering practices: isolate raw ingestion from transformations; express transformations in version-controlled SQL models; test assumptions before publishing; and separate the analytics artifact from a transient build-time warehouse.

There are important limits. The data are synthetic, so this example does not ingest a live commercial API. The scheduled job regenerates the same seeded demonstration data; it does not capture real-time transactions. The database does not persist between ephemeral CI runs. For a production environment, these components could be replaced with authenticated connectors, persistent object storage, incremental ingestion and stronger observability.

## 11. Conclusion and Repository

**FlowForge DE** shows that an end-to-end data engineering workflow can be explained, tested, automated and shared publicly with freely available tools. The result is more than a visualization: it demonstrates ingestion, reproducible transformations, validation, orchestration, and deployment.

**Source code and CI workflow:** https://github.com/Gino019/automated-data-engineering-project

**Public dashboard (after deployment):** https://gino019.github.io/automated-data-engineering-project/

**GitHub Actions history:** https://github.com/Gino019/automated-data-engineering-project/actions

Thanks for reading. Feedback and contributions are welcome in the public repository.

---

### References

- [dbt Documentation — About dbt](https://docs.getdbt.com/docs/introduction)
- [dbt Documentation — DuckDB adapter](https://docs.getdbt.com/docs/local/connect-data-platform/duckdb-setup)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages — Custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
