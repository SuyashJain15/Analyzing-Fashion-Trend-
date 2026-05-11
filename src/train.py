from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


def train_and_save(clean_csv: Path, artifacts_dir: Path) -> Tuple[float, float]:
    df = pd.read_csv(clean_csv)
    X = df.iloc[:, 0].astype(str)
    y = df['label'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    tfidf = TfidfVectorizer(max_features=30000, ngram_range=(1, 2))

    lr = LogisticRegression(max_iter=1000, n_jobs=None, solver='liblinear')
    rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)

    # Fit vectorizer
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec = tfidf.transform(X_test)

    lr.fit(X_train_vec, y_train)
    rf.fit(X_train_vec, y_train)

    lr_acc = accuracy_score(y_test, lr.predict(X_test_vec))
    rf_acc = accuracy_score(y_test, rf.predict(X_test_vec))

    artifacts_dir.mkdir(exist_ok=True)
    joblib.dump(tfidf, artifacts_dir / 'tfidf.pkl')
    joblib.dump(lr, artifacts_dir / 'logreg.pkl')
    joblib.dump(rf, artifacts_dir / 'random_forest.pkl')

    return lr_acc, rf_acc



