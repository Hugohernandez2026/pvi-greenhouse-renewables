"""
Predictive Viability Index (PVI) pipeline for greenhouse renewable systems.

Stages:
  1) Load features and configuration catalog
  2) Estimate P(NPV > 0) (empirical or ML)
  3) Compute ENPV = NPV0 + option value
  4) Rank with PVI = alpha * s(p_hat) + (1-alpha) * s(ENPV)

MIT License — illustrative research code. Recalibrate on local data before use.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def minmax(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    lo, hi = float(np.min(x)), float(np.max(x))
    if hi - lo < 1e-12:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)


def load_assumptions(path: Optional[Path] = None) -> dict:
    path = path or DATA / "assumptions.json"
    return json.loads(path.read_text())


def load_configurations(path: Optional[Path] = None) -> pd.DataFrame:
    path = path or DATA / "configurations.csv"
    return pd.read_csv(path)


def load_training_samples(path: Optional[Path] = None) -> pd.DataFrame:
    path = path or DATA / "ml_training_samples.csv"
    return pd.read_csv(path)


def empirical_ranking(samples: pd.DataFrame, configs: pd.DataFrame, alpha: float = 0.5) -> pd.DataFrame:
    """Aggregate Monte-Carlo samples into PVI ranking by configuration."""
    g = samples.groupby("config_id").agg(
        p_hat=("positive_npv", "mean"),
        npv_mean=("npv", "mean"),
        enpv_mean=("enpv", "mean"),
        n=("positive_npv", "count"),
    ).reset_index()
    g = g.merge(configs[["config_id", "name", "capacity_kw", "staged"]], on="config_id", how="left")
    g["PVI"] = alpha * minmax(g["p_hat"].values) + (1 - alpha) * minmax(g["enpv_mean"].values)
    g = g.sort_values("PVI", ascending=False).reset_index(drop=True)
    g["rank"] = np.arange(1, len(g) + 1)
    return g


def pvi_vector(p_hat: np.ndarray, enpv: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    return alpha * minmax(p_hat) + (1.0 - alpha) * minmax(enpv)


def option_share_table(path: Optional[Path] = None) -> pd.DataFrame:
    path = path or DATA / "volatility_sensitivity.csv"
    return pd.read_csv(path)


def co2_illustration(path: Optional[Path] = None) -> dict:
    path = path or DATA / "co2_illustration.json"
    return json.loads(path.read_text())


def run_pipeline(alpha: float = 0.5, export: bool = True) -> pd.DataFrame:
    configs = load_configurations()
    samples = load_training_samples()
    ranking = empirical_ranking(samples, configs, alpha=alpha)
    if export:
        out = DATA / "pvi_ranking_summary.csv"
        ranking.to_csv(out, index=False)
        print(f"Wrote {out}")
    return ranking


def main() -> None:
    print("=== PVI greenhouse pipeline ===")
    ranking = run_pipeline(alpha=0.5)
    print(ranking[["rank", "name", "p_hat", "enpv_mean", "PVI"]].to_string(index=False))
    print("\nVolatility sensitivity:")
    print(option_share_table().to_string(index=False))
    print("\nCO2 illustration:")
    for k, v in co2_illustration().items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
