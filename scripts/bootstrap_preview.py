"""Dependency-free demo JSON. On deployment, replaced with verified dbt/DuckDB output."""
import csv
import json
from collections import defaultdict
from pathlib import Path
from scripts.generate_data import generate


def preview(csv_dir: Path, dest: Path) -> None:
    generate(csv_dir)
    def load(name):
        with (csv_dir / f'{name}.csv').open(newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    orders, customers, products = load('orders'), load('customers'), load('products')
    customer_region = {r['customer_id']: r['region'] for r in customers}
    prod_category = {r['product_id']: (r['category'], float(r['unit_cost'])) for r in products}
    cube = defaultdict(lambda: {'orders': 0, 'units': 0, 'revenue': 0, 'profit': 0})
    completed = 0
    for order in orders:
        if order['status'] != 'completed':
            continue
        completed += 1
        cat, unit_cost = prod_category[order['product_id']]
        month = order['order_ts'][:7]
        key = (month, int(month[:4]), customer_region[order['customer_id']], cat)
        q = int(order['quantity'])
        revenue = round(q * float(order['unit_price']), 2)
        cost = round(q * unit_cost, 2)
        group = cube[key]
        group['orders'] += 1
        group['units'] += q
        group['revenue'] += revenue
        group['profit'] += round(revenue - cost, 2)
    rows = []
    for (month, year, region, category), sums in sorted(cube.items()):
        rows.append({'month': month, 'year': year, 'region': region,
                     'category': category, **{k: round(v, 2) for k, v in sums.items()}})
    payload = {'project': 'FlowForge DE', 'source': 'synthetic preview (dbt pipeline replaces this during CI)',
               'synthetic': True, 'generated_at_utc': 'PREVIEW ONLY', 'run_id': 'preview',
               'quality': {'raw_orders': len(orders), 'customers': len(customers),
                           'products': len(products), 'completed_orders': completed,
                           'excluded_cancelled_or_refunded': len(orders) - completed}, 'rows': rows}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    print(f'Preview created: {len(rows)} aggregated cube rows; {completed} completed sales')


if __name__ == '__main__':
    preview(Path('data/raw'), Path('site/data/metrics.json'))
