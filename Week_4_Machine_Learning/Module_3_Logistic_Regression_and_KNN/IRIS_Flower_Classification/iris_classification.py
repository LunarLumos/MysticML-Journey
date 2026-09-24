"""
iris_classification.py
======================
Week 4 · Module 3 – Project: IRIS Flower Classification

Goal: predict the species (setosa / versicolor / virginica) of an iris flower
from 4 measurements (sepal length/width, petal length/width, in cm).

Pipeline
--------
1. Load the classic Iris dataset (bundled with scikit-learn – no download)
2. EDA: class balance, per-species means, pair-plot saved to outputs/
3. Stratified train/test split (80/20)
4. Model A: Logistic Regression (multinomial) with scaling
   Model B: KNN with k chosen by 5-fold cross-validation
5. Evaluate: accuracy, precision, recall, F1, confusion matrix
6. Predict species for a few new flowers

Run:
    python iris_classification.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def load_data() -> tuple[pd.DataFrame, list[str]]:
    """Return the iris data as a DataFrame with a 'species' column."""
    iris = load_iris(as_frame=True)
    df = iris.frame.rename(columns={"target": "species_id"})
    df["species"] = df["species_id"].map(dict(enumerate(iris.target_names)))
    return df, list(iris.feature_names)


def eda(df: pd.DataFrame) -> None:
    """Print a quick overview and save a pair-plot."""
    print("=" * 64)
    print("Exploratory Data Analysis")
    print("=" * 64)
    print(f"[*] Shape: {df.shape} | missing values: {int(df.isnull().sum().sum())}")
    print(df["species"].value_counts().to_string())
    print("\n[*] Mean measurement per species (cm):")
    with pd.option_context("display.width", 120, "display.max_columns", 10):
        print(df.drop(columns="species_id").groupby("species").mean().round(2))
    OUTPUT_DIR.mkdir(exist_ok=True)
    grid = sns.pairplot(df.drop(columns="species_id"), hue="species", height=2)
    out = OUTPUT_DIR / "iris_pairplot.png"
    grid.savefig(out, dpi=100)
    plt.close("all")
    print(f"[*] Pair-plot saved to: {out}  (petal features separate species best)")


def evaluate(name: str, model, X_test, y_test, labels: list[str]) -> float:
    """Print metrics and save a confusion matrix for one model."""
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n--- {name} --- test accuracy = {acc:.3f}")
    print(classification_report(y_test, y_pred, target_names=labels))
    disp = ConfusionMatrixDisplay.from_predictions(y_test, y_pred,
                                                   display_labels=labels, cmap="Greens")
    disp.ax_.set_title(f"Iris – {name}")
    out = OUTPUT_DIR / f"iris_cm_{name.split()[0].lower()}.png"
    plt.tight_layout()
    plt.savefig(out, dpi=110)
    plt.close()
    print(f"[*] Confusion matrix saved to: {out}")
    return acc


def main() -> None:
    """Run the iris classification project end-to-end."""
    df, features = load_data()
    eda(df)
    labels = ["setosa", "versicolor", "virginica"]
    X, y = df[features], df["species_id"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y,
                                              random_state=42)

    logreg = Pipeline([("scale", StandardScaler()),
                       ("clf", LogisticRegression(max_iter=1000))]).fit(X_tr, y_tr)

    knn_search = GridSearchCV(
        Pipeline([("scale", StandardScaler()), ("clf", KNeighborsClassifier())]),
        {"clf__n_neighbors": list(range(1, 26, 2))}, cv=5).fit(X_tr, y_tr)
    print(f"\n[*] Best k for KNN (5-fold CV): {knn_search.best_params_['clf__n_neighbors']}"
          f"  (CV accuracy {knn_search.best_score_:.3f})")

    evaluate("Logistic Regression", logreg, X_te, y_te, labels)
    evaluate("KNN", knn_search.best_estimator_, X_te, y_te, labels)

    new_flowers = pd.DataFrame([[5.0, 3.4, 1.5, 0.2],
                                [6.0, 2.8, 4.5, 1.4],
                                [7.2, 3.1, 6.0, 2.2]], columns=features)
    print("\n[*] Predictions for new flowers (Logistic Regression):")
    for row, pred, proba in zip(new_flowers.values, logreg.predict(new_flowers),
                                logreg.predict_proba(new_flowers)):
        print(f"    {row} → {labels[pred]:<10} (confidence {proba.max():.2%})")


if __name__ == "__main__":
    main()
