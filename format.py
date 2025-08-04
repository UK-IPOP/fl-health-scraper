from pathlib import Path

import polars as pl

pl.read_ndjson(Path().cwd() / "data" / "output.jsonl").sort(
    ["scraped_county", "scraped_year"]
).write_csv(Path().cwd() / "data" / "output.csv")
