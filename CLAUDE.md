# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Medallion Architecture (Bronze → Silver → Gold) data pipeline that extracts e-commerce product data from the fakestoreapi.com API, loads it into PostgreSQL, cleans/transforms it, and aggregates business metrics. Commit messages and script output/print statements in this repo are written in Azerbaijani.

## Commands

Setup (PostgreSQL runs in Docker; everything else runs locally with plain Python — no Airflow/orchestrator is wired up yet, despite the empty `dags/` directory):

```
cp .env.example .env          # fill in real DB credentials (never commit .env)
docker-compose up -d          # start Postgres (localhost:5432, reads config from .env)
pip install -r requirements.txt
```

Running the pipeline is a two-step process — `pipeline.py` does NOT call extraction, so the raw JSON file must exist first:

```
python scripts/extract_products.py   # fetches from fakestoreapi.com, writes data/bronze/products.json
python pipeline.py                   # runs create_tables -> load -> transform -> gold, in order
```

Individual stages can also be run standalone (each script has `if __name__ == "__main__"`):

```
python scripts/create_tables.py
python scripts/load_products.py
python scripts/transform_products.py
python scripts/generate_gold.py
python scripts/check_gold_data.py    # prints the final gold_category_summary table
```

There is no test suite, linter, or formatter configured in this repo.

## Architecture

Data flows through three layers, each backed by its own Postgres table, with one script per stage in `scripts/`:

1. **Bronze** (`extract_products.py` → `load_products.py`): raw API data is fetched and dumped to `data/bronze/products.json`, then loaded verbatim into `bronze_products` (this directory is gitignored — never commit it).
2. **Silver** (`transform_products.py`): reads `bronze_products`, upper-cases `category` into `category_upper`, and upserts into `silver_products` keyed by `id` (`ON CONFLICT ... DO UPDATE`).
3. **Gold** (`generate_gold.py`): aggregates `silver_products` (COUNT, AVG price grouped by `category_upper`) and upserts into `gold_category_summary`.

`pipeline.py` is the orchestrator: it imports each stage's function from `scripts/` (via `sys.path.append`) and runs them in sequence — `create_tables()` → `load_json_to_postgres()` → `transform_and_load_silver()` → `generate_gold_summary()`.

Each script in `scripts/` is self-contained and independently runnable. All of them import `DB_CONFIG` from `scripts/db_config.py`, which loads `DB_HOST`/`DB_PORT`/`DB_NAME`/`DB_USER`/`DB_PASSWORD` from the environment via `python-dotenv` (reads `.env`, which is gitignored — use `.env.example` as the template). `docker-compose.yml` reads the same `.env` file for the Postgres container's credentials, so `.env` is the single source of truth for DB config.

Every stage script follows the same pattern: connect via `psycopg2`, execute the stage's logic in a `try/except` that prints an Azerbaijani error message on failure (no re-raise), then close the cursor/connection. Table upserts use Postgres `ON CONFLICT ... DO UPDATE`, so re-running any stage is idempotent.
