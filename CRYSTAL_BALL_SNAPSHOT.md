# Crystal Ball Intelligence V12 — Operational Snapshot (Sep 2025)

This snapshot records the verified state so we can proceed safely and restore context quickly if needed. Docs-only; no app code changes.

## GCP
- Project: `crystal-ball-intelligence-v12`
- Region: `us-central1`
- Billing: enabled
- Secondary project: `sonorous-summer-472912-c4` — billing disabled; no datasets/buckets; ignore

### BigQuery
- Datasets: `raw`, `curated`, `features`, `forecasts`
- Confirmed curated tables:
  - `curated.futures_daily` (OHLCV; keys: `symbol`, `trade_date`, `close`, …)
  - `curated.weather_indicators` (`date`, `weather_risk_score`, …)
- Buckets: `crystal-ball-intelligence-v12-{marketplace-data,scraping-data,csv-uploads}`

### Vertex AI
- Embeddings endpoint: `embeddinggemma-300m-mg-one-click-deploy` (model: `embeddinggemma-300m`)

## Data policy (UI/API)
- Dashboard must read computed data only (BigQuery views/tables). No direct external feeds.

## Volatility block (IV/HV)
- Correct IV analogue for ZL is CME CVOL Soybean Oil (SOVL), not equity VIX. Until we ingest SOVL, compute a proxy from realized volatility and drivers; later backfill true SOVL.
- Views to add (non-destructive):
  - `features.realized_volatility` — HV 30/60/90d (annualized) from `curated.futures_daily` for `ZL`.
  - `features.vix_sovl_features` — uses `curated.sovl_daily` if present (true IV) else HV proxy; exposes IV−HV spread.
  - `features.crush_spread` — board crush (ZL, ZM, ZS) with 60d z-score.
  - `features.vol_drivers` — joins HV/IV, crush, and weather into one driver panel.
- Table to add (create-only): `curated.sovl_daily(date, iv_30d, source, ingested_at)`.

## Embeddings / RAG
- Env (examples):
  - `VERTEX_PROJECT_ID=crystal-ball-intelligence-v12`
  - `VERTEX_LOCATION=us-central1`
  - `VERTEX_EMBEDDING_ENDPOINT=embeddinggemma-300m-mg-one-click-deploy`
- Storage: `features.news_embeddings(embedding ARRAY<FLOAT64>, …)`; similarity via `1 - COSINE_DISTANCE(embedding, @query_vec)`.

## Data Quality
- Enable BigQuery Data Quality Scans on `curated.*` and `features.*` (completeness, date monotonicity, OHLC constraints, outlier caps). Schedule scans and publish results for audit.

## Guardrails / Safety
- Add-only views/tables; never mutate/delete existing objects.
- UI shows “pipeline empty” banner if required tables have no rows.
- No secrets in repo; configure via environment only.

## Next steps (safe)
1) Create the views/tables listed above (idempotent).
2) Add a Cloud Run Job `sovl-modeler` to write IV proxy rows (`source='modeled:garch'`) into `curated.sovl_daily` until SOVL access is enabled.
3) Wire API to `features.*`/`forecasts.*` exclusively and remove raw external fallbacks.
4) Enable BigQuery DQ scans and alerts.
