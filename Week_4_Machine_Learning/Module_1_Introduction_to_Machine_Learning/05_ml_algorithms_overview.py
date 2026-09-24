"""
05_ml_algorithms_overview.py
============================
Week 4 · Module 1 – Different ML Algorithms

A quick "tour" that trains many common algorithms on the SAME datasets so you can
see that the scikit-learn API is always the same:  model.fit(X, y) → model.predict(X)

  • Classification: breast-cancer dataset (bundled with scikit-learn)
  • Regression    : diabetes dataset       (bundled with scikit-learn)

Scores are 5-fold cross-validation means (explained in Module 7).

Run:
    python 05_ml_algorithms_overview.py
"""

import time

from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.ensemble import (GradientBoostingClassifier, GradientBoostingRegressor,
                              RandomForestClassifier, RandomForestRegressor)
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression, Ridge
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


def scaled(model):
    """Wrap distance/gradient-based models with a StandardScaler."""
    return make_pipeline(StandardScaler(), model)


CLASSIFIERS = {
    "Logistic Regression": scaled(LogisticRegression(max_iter=1000)),
    "K-Nearest Neighbors": scaled(KNeighborsClassifier()),
    "Naive Bayes": GaussianNB(),
    "Decision Tree": DecisionTreeClassifier(random_state=0),
    "Random Forest": RandomForestClassifier(random_state=0),
    "Gradient Boosting": GradientBoostingClassifier(random_state=0),
    "Support Vector Machine": scaled(SVC()),
}

REGRESSORS = {
    "Linear Regression": LinearRegression(),
    "Ridge (L2)": Ridge(),
    "Lasso (L1)": Lasso(alpha=0.1),
    "K-Nearest Neighbors": scaled(KNeighborsRegressor()),
    "Decision Tree": DecisionTreeRegressor(random_state=0, max_depth=4),
    "Random Forest": RandomForestRegressor(random_state=0),
    "Gradient Boosting": GradientBoostingRegressor(random_state=0),
    "Support Vector Regr.": scaled(SVR(C=100)),
}


def benchmark(models: dict, X, y, scoring: str, title: str) -> None:
    """Cross-validate every model and print a ranked table."""
    print("=" * 60)
    print(title)
    print("=" * 60)
    results = []
    for name, model in models.items():
        start = time.perf_counter()
        score = cross_val_score(model, X, y, cv=5, scoring=scoring).mean()
        results.append((name, score, time.perf_counter() - start))
    for name, score, secs in sorted(results, key=lambda r: r[1], reverse=True):
        print(f"[+] {name:<24} {scoring}={score:.3f}   ({secs:.2f}s)")
    print()


def main() -> None:
    """Benchmark classifiers and regressors on bundled datasets."""
    X_c, y_c = load_breast_cancer(return_X_y=True)
    benchmark(CLASSIFIERS, X_c, y_c, "accuracy",
              "CLASSIFICATION · breast cancer (malignant vs benign)")
    X_r, y_r = load_diabetes(return_X_y=True)
    benchmark(REGRESSORS, X_r, y_r, "r2",
              "REGRESSION · diabetes disease progression")
    print("[*] Lesson: no single algorithm always wins ('No Free Lunch').")
    print("    Always compare a few candidates with cross-validation.")


if __name__ == "__main__":
    main()
