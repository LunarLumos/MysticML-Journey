"""
ml_workflow_demo.py
===================
Week 4 · Module 1 – Introduction to Machine Learning

An END-TO-END walk through the "Flow of Machine Learning":

    1. Define the problem        -> "Which cultivar is this wine?"  (classification)
    2. Collect the data          -> sklearn's bundled Wine dataset (no network needed)
    3. Explore the data (EDA)    -> shape, types, class balance, summary stats
    4. Prepare the data          -> train/test split + feature scaling
    5. Choose & train a model    -> baseline vs. Logistic Regression vs. Random Forest
    6. Evaluate                  -> accuracy, confusion matrix, classification report
    7. Improve / select          -> pick the best model with cross-validation
    8. Deploy (simulated)        -> save the model with joblib, reload it, predict

Run:
    python ml_workflow_demo.py
"""

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


# ---------------------------------------------------------------
# Step 1 + 2: Problem definition & data collection
# ---------------------------------------------------------------
def load_data() -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Load the Wine dataset as a pandas DataFrame + target Series."""
    wine = load_wine(as_frame=True)
    return wine.data, wine.target, list(wine.target_names)


# ---------------------------------------------------------------
# Step 3: Exploratory Data Analysis
# ---------------------------------------------------------------
def explore(X: pd.DataFrame, y: pd.Series, class_names: list[str]) -> None:
    """Print the most important facts about the dataset."""
    print("=" * 60)
    print("STEP 3 · Exploratory Data Analysis")
    print("=" * 60)
    print(f"[*] Rows (samples): {X.shape[0]}  |  Columns (features): {X.shape[1]}")
    print(f"[*] Missing values in total: {int(X.isnull().sum().sum())}")
    print("[*] Class balance:")
    for idx, count in y.value_counts().sort_index().items():
        print(f"    {class_names[idx]:<8} -> {count} samples")
    print("\n[*] First 5 rows (first 5 columns):")
    print(X.iloc[:5, :5])
    print("\n[*] Summary statistics (first 5 columns):")
    print(X.iloc[:, :5].describe().round(2))


# ---------------------------------------------------------------
# Step 4 → 7: Prepare, train, evaluate, select
# ---------------------------------------------------------------
def build_candidates() -> dict:
    """Return the candidate models we want to compare."""
    return {
        # A 'dummy' model that always predicts the most common class.
        # Any real model MUST beat this, otherwise it learned nothing.
        "Baseline (most frequent)": DummyClassifier(strategy="most_frequent"),
        # Scaling lives INSIDE the pipeline, so it is learned only from training data.
        "Logistic Regression": make_pipeline(StandardScaler(),
                                             LogisticRegression(max_iter=1000)),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    }


def train_and_select(X_train, y_train) -> tuple[str, object]:
    """Compare candidates with 5-fold cross-validation and return the best one."""
    print("\n" + "=" * 60)
    print("STEP 5 + 7 · Train candidates & select with 5-fold cross-validation")
    print("=" * 60)
    best_name, best_score, best_model = None, -1.0, None
    for name, model in build_candidates().items():
        scores = cross_val_score(model, X_train, y_train, cv=5)
        print(f"[+] {name:<26} CV accuracy = {scores.mean():.3f} ± {scores.std():.3f}")
        if scores.mean() > best_score:
            best_name, best_score, best_model = name, scores.mean(), model
    print(f"\n[*] Selected model: {best_name}")
    best_model.fit(X_train, y_train)  # re-fit on the full training set
    return best_name, best_model


def evaluate(model, X_test, y_test, class_names: list[str], title: str) -> None:
    """Evaluate on the held-out TEST set (data the model has never seen)."""
    print("\n" + "=" * 60)
    print("STEP 6 · Evaluate on the untouched test set")
    print("=" * 60)
    y_pred = model.predict(X_test)
    print(f"[*] Test accuracy: {accuracy_score(y_test, y_pred):.3f}\n")
    print(classification_report(y_test, y_pred, target_names=class_names))

    OUTPUT_DIR.mkdir(exist_ok=True)
    disp = ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=class_names, cmap="Blues")
    disp.ax_.set_title(f"Confusion Matrix – {title}")
    out = OUTPUT_DIR / "workflow_confusion_matrix.png"
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"[*] Confusion matrix saved to: {out}")


# ---------------------------------------------------------------
# Step 8: "Deployment" – persist and reuse the model
# ---------------------------------------------------------------
def deploy(model, X_test: pd.DataFrame, class_names: list[str]) -> None:
    """Save the model to disk, load it back and predict a 'new' sample."""
    print("\n" + "=" * 60)
    print("STEP 8 · Save → load → predict (simulated deployment)")
    print("=" * 60)
    OUTPUT_DIR.mkdir(exist_ok=True)
    model_path = OUTPUT_DIR / "wine_model.joblib"
    joblib.dump(model, model_path)
    print(f"[*] Model saved to: {model_path}")

    loaded = joblib.load(model_path)
    new_sample = X_test.iloc[[0]]  # pretend this arrived from a user
    pred = loaded.predict(new_sample)[0]
    print(f"[*] Prediction for a new wine sample: {class_names[pred]}")


def main() -> None:
    """Run the whole ML workflow step by step."""
    X, y, class_names = load_data()
    explore(X, y, class_names)

    print("\n" + "=" * 60)
    print("STEP 4 · Split the data (80% train / 20% test, stratified)")
    print("=" * 60)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)
    print(f"[*] Train: {X_train.shape}  |  Test: {X_test.shape}")

    best_name, best_model = train_and_select(X_train, y_train)
    evaluate(best_model, X_test, y_test, class_names, best_name)
    deploy(best_model, X_test, class_names)


if __name__ == "__main__":
    main()
