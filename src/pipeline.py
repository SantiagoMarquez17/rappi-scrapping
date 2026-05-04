from __future__ import annotations

import argparse
import logging

import pandas as pd

from src.analysis import build_competitive_index, clean, generate_charts, write_insights
from src.collectors import get_collectors
from src.config import PROCESSED_DIR, RAW_DIR


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def run(mode: str) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for collector in get_collectors(mode):
        logging.info("Collecting platform=%s mode=%s", collector.platform, mode)
        try:
            rows.extend(collector.collect())
        except NotImplementedError as exc:
            logging.warning("%s", exc)
        except Exception:
            logging.exception("Collector failed for %s", collector.platform)

    if not rows:
        raise RuntimeError("No rows collected. Use --mode sample for the reproducible demo path.")

    raw_df = pd.DataFrame(rows)
    raw_path = RAW_DIR / "competitive_raw.csv"
    raw_df.to_csv(raw_path, index=False)
    logging.info("Wrote raw output: %s", raw_path)

    clean_df = clean(raw_df)
    clean_path = PROCESSED_DIR / "competitive_clean.csv"
    clean_df.to_csv(clean_path, index=False)
    logging.info("Wrote clean output: %s", clean_path)

    competitive = build_competitive_index(clean_df)
    competitive_path = PROCESSED_DIR / "competitive_index.csv"
    competitive.to_csv(competitive_path, index=False)
    logging.info("Wrote competitive index: %s", competitive_path)

    generate_charts(clean_df, competitive)
    insights_path = write_insights(clean_df, competitive)
    logging.info("Wrote insights: %s", insights_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rappi competitive intelligence pipeline")
    parser.add_argument("--mode", choices=["sample", "live"], default="sample")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.mode)
