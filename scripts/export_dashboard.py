"""Publish small aggregates (never customer-level data) as static JSON for GitHub Pages."""
from __future__ import annotations
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def export(database: Path, dest: Path) -> dict:
    import duckdb
    con = duckdb.connect(str(database), read_only=True)
    try:
        cube_rows = con.execute('''
          SELECT strftime(month_start, '%Y-%m') AS month, year, region, category,
                 CAST(order_count AS INTEGER), CAST(units_sold AS INTEGER),
                 CAST(revenue AS DOUBLE), CAST(profit AS DOUBLE)
          FROM analytics_marts.mart_sales_cube
          ORDER BY 1, 3, 4
        ''').fetchall()
        stats = con.execute('''
          SELECT
            (SELECT count(*) FROM raw.orders),
            (SELECT count(*) FROM raw.customers),
            (SELECT count(*) FROM raw.products),
            (SELECT count(*) FROM analytics_marts.fct_completed_orders)
        ''').fetchone()
        payload = {
            'project': 'FlowForge DE',
            'source': 'dbt-duckdb automated ELT pipeline',
            'synthetic': True,
            'generated_at_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'run_id': os.environ.get('GITHUB_RUN_ID', 'local'),
            'quality': {'raw_orders': stats[0], 'customers': stats[1],
                        'products': stats[2], 'completed_orders': stats[3],
                        'excluded_cancelled_or_refunded': stats[0] - stats[3]},
            'rows': [
                {'month': r[0], 'year': r[1], 'region': r[2], 'category': r[3],
                 'orders': r[4], 'units': r[5], 'revenue': round(r[6], 2),
                 'profit': round(r[7], 2)} for r in cube_rows
            ]
        }
        assert payload['rows'], 'No dbt mart results produced'
        assert sum(r['orders'] for r in payload['rows']) == stats[3], 'mart facts do not reconcile'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
        return payload
    finally:
        con.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='warehouse/flowforge.duckdb')
    parser.add_argument('--out', default='site/data/metrics.json')
    args = parser.parse_args()
    payload = export(Path(args.db), Path(args.out))
    print(f"Published {len(payload['rows'])} cube rows / {payload['quality']['completed_orders']} completed orders")
