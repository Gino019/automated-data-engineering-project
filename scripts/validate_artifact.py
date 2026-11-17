"""Fail CI if the published artifact is missing, incoherent or still a preview."""
import json
from pathlib import Path
p = json.loads(Path('site/data/metrics.json').read_text(encoding='utf-8'))
assert p['source'] == 'dbt-duckdb automated ELT pipeline', 'CI must replace the preview'
assert len(p['rows']) > 40, 'Too few aggregates produced'
assert sum(r['orders'] for r in p['rows']) == p['quality']['completed_orders']
assert p['quality']['raw_orders'] == 3200
assert all(r['revenue'] >= 0 and r['orders'] > 0 for r in p['rows'])
print('Artifact validated:', len(p['rows']), 'monthly-region-category aggregate rows')
