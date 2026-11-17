"""Reproducible, entirely synthetic e-commerce CSV source extracts."""
from __future__ import annotations
import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

REGIONS = ['North', 'South', 'East', 'West', 'Central']
CATEGORIES = ['Electronics', 'Home', 'Sports', 'Fashion']
START = datetime(2025, 1, 1, 8)
END = datetime(2026, 10, 31, 20)


def generate(output_dir: Path, count: int = 3200, seed: int = 2026) -> dict[str, int]:
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    customers = [{'customer_id': i, 'region': REGIONS[(i * 7 + i // 9) % len(REGIONS)],
                  'segment': ['Consumer', 'Corporate', 'Small Business'][i % 3]}
                 for i in range(1, 261)]
    products = []
    for i in range(1, 49):
        category = CATEGORIES[(i - 1) % len(CATEGORIES)]
        price = round(rng.uniform(18, 480), 2)
        products.append({'product_id': i, 'product_name': f'{category} Item {i:02d}',
                         'category': category, 'unit_cost': f'{price * rng.uniform(.48, .77):.2f}',
                         'list_price': f'{price:.2f}'})
    orders = []
    for i in range(1, count + 1):
        customer = rng.choice(customers)
        product = rng.choice(products)
        ts = START + timedelta(seconds=rng.randrange(int((END - START).total_seconds())))
        status = rng.choices(['completed', 'cancelled', 'refunded'], weights=[.88, .08, .04])[0]
        quantity = rng.randint(1, 5)
        unit_price = round(float(product['list_price']) * rng.uniform(.86, 1.04), 2)
        orders.append({'order_id': i, 'order_ts': ts.strftime('%Y-%m-%d %H:%M:%S'),
                       'customer_id': customer['customer_id'], 'product_id': product['product_id'],
                       'quantity': quantity, 'unit_price': f'{unit_price:.2f}', 'status': status})
    def write(filename: str, rows: list[dict]) -> None:
        with (output_dir / filename).open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    write('customers.csv', customers)
    write('products.csv', products)
    write('orders.csv', orders)
    return {'orders': len(orders), 'customers': len(customers), 'products': len(products)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='data/raw')
    parser.add_argument('--count', type=int, default=3200)
    parser.add_argument('--seed', type=int, default=2026)
    args = parser.parse_args()
    print(generate(Path(args.out), count=args.count, seed=args.seed))
