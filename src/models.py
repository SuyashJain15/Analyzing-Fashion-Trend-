from pathlib import Path
from typing import Tuple

import joblib
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / 'artifacts'


def load_models():
    tfidf = joblib.load(ARTIFACTS_DIR / 'tfidf.pkl')
    lr = joblib.load(ARTIFACTS_DIR / 'logreg.pkl')
    rf = joblib.load(ARTIFACTS_DIR / 'random_forest.pkl')
    return {'tfidf': tfidf, 'lr': lr, 'rf': rf}


def predict_text(models, text: str) -> Tuple[int, float, int, float, int]:
    vec = models['tfidf'].transform([text])
    lr_prob = float(models['lr'].predict_proba(vec)[0, 1]) if hasattr(models['lr'], 'predict_proba') else float(models['lr'].decision_function(vec))
    rf_prob = float(models['rf'].predict_proba(vec)[0, 1]) if hasattr(models['rf'], 'predict_proba') else float(models['rf'].decision_function(vec))
    lr_pred = int(lr_prob >= 0.5)
    rf_pred = int(rf_prob >= 0.5)
    ensemble = int((lr_pred + rf_pred) >= 1)
    return lr_pred, lr_prob, rf_pred, rf_prob, ensemble



