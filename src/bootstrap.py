import json
import os
from pathlib import Path
from typing import Tuple

from .data_prep import ensure_kaggle_download, preprocess_reviews
from .train import train_and_save


BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / 'artifacts'
DATA_DIR = BASE_DIR / 'data'

ARTIFACTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


def artifacts_exist() -> bool:
    lr = ARTIFACTS_DIR / 'logreg.pkl'
    rf = ARTIFACTS_DIR / 'random_forest.pkl'
    vocab = ARTIFACTS_DIR / 'tfidf.pkl'
    trends = ARTIFACTS_DIR / 'top_trends.json'
    return lr.exists() and rf.exists() and vocab.exists() and trends.exists()


def ensure_artifacts() -> None:
    if artifacts_exist():
        return

    # Download subset of Kaggle dataset and preprocess
    csv_path = ensure_kaggle_download(DATA_DIR)
    clean_csv, top_trends = preprocess_reviews(csv_path, DATA_DIR)

    # Train models and persist
    train_and_save(clean_csv, ARTIFACTS_DIR)

    # Save trends for suggestions
    (ARTIFACTS_DIR / 'top_trends.json').write_text(
        json.dumps(top_trends, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )



