"""E: extract generated CSVs; L: load them into a local DuckDB raw schema."""
from __future__ import annotations
import argparse
from pathlib import Path


def ingest(csv_dir: Path, database: Path) -> dict[str, int]:
    import duckdb
    database.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(database))
    try:
        con.execute('CREATE SCHEMA IF NOT EXISTS raw')
        result = {}
        for table in ('orders', 'customers', 'products'):
            csv_path = csv_dir / f'{table}.csv'
            if not csv_path.is_file():
                raise FileNotFoundError(f'Missing source extract: {csv_path}')
            # Path is locally generated and not user-supplied in the workflow.
            con.execute(f'CREATE OR REPLACE TABLE raw.{table} AS SELECT * FROM read_csv_auto(?, HEADER=TRUE)', [str(csv_path)])
            result[table] = con.execute(f'SELECT count(*) FROM raw.{table}').fetchone()[0]
            if not result[table]:
                raise ValueError(f'No rows loaded: raw.{table}')
        return result
    finally:
        con.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-dir', default='data/raw')
    parser.add_argument('--db', default='warehouse/flowforge.duckdb')
    args = parser.parse_args()
    print(ingest(Path(args.csv_dir), Path(args.db)))
