"""
Illustrative Predictive Viability Index (PVI) ranking for greenhouse
renewable configurations under energy-price uncertainty.

Demonstration only — recalibrate on local metered loads and tariffs
before operational use. Pure NumPy/pandas version (no scikit-learn required).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)


def minmax(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    lo, hi = x.min(), x.max()
    if hi - lo < 1e-12:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)


def configuration_table() -> pd.DataFrame:
    rows = [
        ("Mid-scale, staged PV", 0.79, 1.00),
        ("PV + heat pump, staged", 0.77, 0.95),
        ("Minimal, staged PV", 0.72, 0.81),
        ("Mid-scale, full PV", 0.65, 0.70),
        ("Large, full PV", 0.51, 0.56),
    ]
    return pd.DataFrame(rows, columns=["configuration", "p_hat", "enpv_rel"])


def pvi(p_hat: np.ndarray, enpv: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    return alpha * minmax(p_hat) + (1.0 - alpha) * minmax(enpv)


def option_value_share(volatility: str) -> float:
    return {"low": 0.11, "base": 0.26, "high": 0.39}[volatility]


def main() -> None:
    cfg = configuration_table()
    cfg["PVI"] = pvi(cfg["p_hat"].values, cfg["enpv_rel"].values, alpha=0.5)
    cfg["rank"] = cfg["PVI"].rank(ascending=False).astype(int)
    cfg = cfg.sort_values("rank")
    print("PVI ranking (alpha = 0.5) — illustrative greenhouse configurations\n")
    print(cfg.to_string(index=False))
    print("\nOption-value share of ENPV by energy-price volatility:")
    for v in ("low", "base", "high"):
        print(f"  {v:4s}: {option_value_share(v):.2f}")
    print("\nNote: Apply local load and tariff calibration before operational decisions.")


if __name__ == "__main__":
    main()
