import os
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from django.conf import settings

DATA_DIR = os.path.join(settings.BASE_DIR, "data")

def load_csv(name: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    return pd.read_csv(path)

def preview_csv(name: str, limit: int = 50) -> List[Dict[str, Any]]:
    df = load_csv(name)
    return df.head(limit).to_dict(orient="records")

def summary_stats(name: str, include: List[str] | None = None) -> Dict[str, Dict[str, float]]:
    df = load_csv(name)
    if include:
        existing_cols = [c for c in include if c in df.columns]
        df = df[existing_cols]
    desc = df.describe(include="all").fillna("").to_dict()
    result: Dict[str, Dict[str, float]] = {}
    for col, stats in desc.items():
       result[col] = {
    k: (float(v) if isinstance(v, (int, float, np.number)) else v)
    for k, v in stats.items()}
    return result

def groupby_agg(name: str, by: str, agg_col: str, agg_fn: str = "count") -> List[Dict[str, Any]]:
    df = load_csv(name)
    if agg_fn == "count":
        grp = df.groupby(by)[agg_col].count().reset_index(name="value")
    elif agg_fn == "sum":
        grp = df.groupby(by)[agg_col].sum().reset_index(name="value")
    elif agg_fn == "mean":
        grp = df.groupby(by)[agg_col].mean().reset_index(name="value")
    else:
        raise ValueError("Unsupported agg_fn")
    return grp.to_dict(orient="records")

def histogram(name: str, col: str, bins: int = 10) -> Dict[str, List[float]]:
    df = load_csv(name)
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found")
    s = pd.to_numeric(df[col], errors="coerce").dropna()
    counts, bin_edges = np.histogram(s, bins=bins)
    return {
        "counts": counts.tolist(),
        "bins": bin_edges.tolist()
    }
