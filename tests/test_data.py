import csv
from pathlib import Path
from scripts.generate_data import generate
from scripts.bootstrap_preview import preview
import json


def read(path: Path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def test_seed_is_deterministic(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    generate(a, count=90)
    generate(b, count=90)
    for f in ('orders.csv', 'customers.csv', 'products.csv'):
        assert (a / f).read_bytes() == (b / f).read_bytes()


def test_orders_reference_valid_dimensions(tmp_path):
    generate(tmp_path, count=250)
    customers = {x['customer_id'] for x in read(tmp_path / 'customers.csv')}
    products = {x['product_id'] for x in read(tmp_path / 'products.csv')}
    orders = read(tmp_path / 'orders.csv')
    assert len({x['order_id'] for x in orders}) == len(orders)
    assert all(x['customer_id'] in customers and x['product_id'] in products for x in orders)


def test_preview_reconciles_source(tmp_path):
    preview(tmp_path / 'raw', tmp_path / 'metrics.json')
    data = json.loads((tmp_path / 'metrics.json').read_text())
    assert sum(x['orders'] for x in data['rows']) == data['quality']['completed_orders']
    assert data['quality']['raw_orders'] == 3200
    assert all(x['revenue'] > 0 for x in data['rows'])
    assert set(x['category'] for x in data['rows']) == {'Electronics', 'Home', 'Sports', 'Fashion'}


def test_no_personal_data_in_aggregate(tmp_path):
    preview(tmp_path / 'raw', tmp_path / 'metrics.json')
    p = json.loads((tmp_path / 'metrics.json').read_text())
    assert all('customer_id' not in item and 'product_name' not in item for item in p['rows'])


def test_status_domain(tmp_path):
    generate(tmp_path, count=200)
    assert {x['status'] for x in read(tmp_path / 'orders.csv')} <= {'completed', 'cancelled', 'refunded'}
