import json
import os
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi


KAGGLE_DATASET = 'fawadhossaini1415/amazon-fashion-800k-user-reviews-dataset'


def ensure_kaggle_download(data_dir: Path) -> Path:
    """Download dataset using Kaggle Python API and return a CSV path.

    This authenticates using datasets/kaggle.json (copied to ~/.kaggle/kaggle.json),
    downloads and unzips files into data/kaggle_raw, and returns the first CSV found.
    """
    data_dir.mkdir(exist_ok=True)

    # Prepare Kaggle credentials from project's datasets/kaggle.json
    project_root = data_dir.parent
    datasets_dir = project_root / 'datasets'
    kaggle_json = datasets_dir / 'kaggle.json'
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    target = kaggle_dir / 'kaggle.json'
    if kaggle_json.exists():
        target.write_text(kaggle_json.read_text(encoding='utf-8'), encoding='utf-8')
        try:
            os.chmod(target, 0o600)
        except Exception:
            # Windows may not support chmod in the same way; safe to ignore
            pass
    else:
        raise FileNotFoundError('datasets/kaggle.json not found. Please add your Kaggle API token there.')

    # Authenticate and download via API
    api = KaggleApi()
    api.authenticate()

    out_dir = data_dir / 'kaggle_raw'
    out_dir.mkdir(exist_ok=True)

    # Download full dataset folder and unzip
    api.dataset_download_files(KAGGLE_DATASET, path=str(out_dir), unzip=True)

    # Find a reviews CSV; pick the largest (more complete) to use directly
    candidates = list(out_dir.rglob('*.csv'))
    if not candidates:
        raise FileNotFoundError('No CSV files found after Kaggle download')
    csv_path = max(candidates, key=lambda p: p.stat().st_size)
    return csv_path


def preprocess_reviews(csv_path: Path, data_dir: Path) -> Tuple[Path, Dict[str, list]]:
    # Read a subset for speed
    df = pd.read_csv(csv_path)
    # Expect columns like: reviewText, summary, overall, asin, category, brand, color if available
    text_cols = [c for c in ['reviewText', 'summary', 'review_text', 'title'] if c in df.columns]
    if not text_cols:
        # Create a synthetic text field from any available columns
        df['text'] = df.apply(lambda r: ' '.join([str(v) for v in r.values]), axis=1)
        text_col = 'text'
    else:
        text_col = text_cols[0]

    # Heuristic label: consider ratings >= 4 as trending(1), <=2 as not trending(0); drop others
    rating_col = next((c for c in ['overall', 'rating', 'stars'] if c in df.columns), None)
    if rating_col is None:
        # If no rating, mark all as neutral 1 to allow training; not ideal but keeps demo working
        df['label'] = 1
    else:
        df = df[df[rating_col].notna()]
        df['label'] = df[rating_col].apply(lambda x: 1 if x >= 4 else (0 if x <= 2 else None))
        df = df[df['label'].isin([0, 1])]

    # Keep only necessary columns and sample for speed
    df = df[[text_col, 'label']].dropna()
    if len(df) > 50000:
        df = df.sample(50000, random_state=42)

    clean_path = data_dir / 'clean_reviews.csv'
    df.to_csv(clean_path, index=False)

    # Extract trending tokens and colors for suggestions
    tokens = (
        df[text_col]
        .astype(str)
        .str.lower()
        .str.replace(r"[^a-z\s]", " ", regex=True)
        .str.split()
    )
    word_counts: Dict[str, int] = {}
    for arr in tokens:
        for w in arr:
            word_counts[w] = word_counts.get(w, 0) + 1

    popular_items = [w for w in ['jeans', 'tshirt', 'shirt', 'jacket', 'dress', 'sneakers', 'shoes', 'hoodie', 'watch', 'bag'] if w in word_counts]
    popular_items = sorted(popular_items, key=lambda w: -word_counts[w])[:5]
    popular_colors = [w for w in ['black', 'white', 'blue', 'red', 'green', 'beige', 'brown', 'grey', 'pink', 'purple'] if w in word_counts]
    popular_colors = sorted(popular_colors, key=lambda w: -word_counts[w])[:5]

    top_trends = {"items": popular_items, "colors": popular_colors}
    return clean_path, top_trends


