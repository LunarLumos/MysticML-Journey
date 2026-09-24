"""
01_supervised_learning_examples.py
==================================
Week 4 · Module 1 – Machine Learning Types → SUPERVISED LEARNING

Supervised learning = we train on examples that come WITH the right answer
(the "label"). The model learns a mapping  X (features) → y (label).

Two flavours, both shown here:
  • Regression      -> the label is a NUMBER     (e.g. house price)
  • Classification  -> the label is a CATEGORY   (e.g. spam / not spam)

Run:
    python 01_supervised_learning_examples.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, export_text

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


# ---------------------------------------------------------------
# Example 1: Regression – predict exam score from hours studied
# ---------------------------------------------------------------
def regression_example() -> None:
    """Fit a line to (hours studied → exam score) and predict new students."""
    print("=" * 60)
    print("Example 1 · Supervised REGRESSION: hours studied → exam score")
    print("=" * 60)
    rng = np.random.default_rng(42)
    hours = rng.uniform(0, 10, 40).reshape(-1, 1)             # feature X
    score = 35 + 6 * hours.ravel() + rng.normal(0, 4, 40)    # label y (+noise)

    model = LinearRegression().fit(hours, score)             # LEARN from labelled data
    print(f"[*] Learned rule: score ≈ {model.intercept_:.1f} + {model.coef_[0]:.2f} × hours")
    for h in (2, 5, 9):
        print(f"[+] A student who studies {h} h is predicted to score "
              f"{model.predict([[h]])[0]:.1f}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    xs = np.linspace(0, 10, 50).reshape(-1, 1)
    plt.scatter(hours, score, label="training examples (labelled)")
    plt.plot(xs, model.predict(xs), color="red", label="learned model")
    plt.xlabel("Hours studied")
    plt.ylabel("Exam score")
    plt.title("Supervised regression")
    plt.legend()
    out = OUTPUT_DIR / "supervised_regression.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"[*] Plot saved to: {out}\n")


# ---------------------------------------------------------------
# Example 2: Classification – is this e-mail spam?
# ---------------------------------------------------------------
def classification_example() -> None:
    """Train a tiny decision tree on hand-made e-mail features."""
    print("=" * 60)
    print("Example 2 · Supervised CLASSIFICATION: is an e-mail spam?")
    print("=" * 60)
    # Features: [number of links, number of "$" signs, sender is in contacts (1/0)]
    X = np.array([
        [0, 0, 1], [1, 0, 1], [0, 1, 1], [2, 0, 1], [1, 1, 1], [0, 0, 0],
        [8, 5, 0], [6, 3, 0], [9, 7, 0], [5, 6, 0], [7, 2, 0], [4, 4, 0],
    ])
    y = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])  # 0 = ham, 1 = spam
    feature_names = ["links", "dollar_signs", "known_sender"]

    tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)
    print("[*] The rules the tree learned from the labelled examples:")
    print(export_text(tree, feature_names=feature_names))

    new_emails = np.array([[1, 0, 1], [10, 8, 0], [3, 3, 0]])
    for email, pred in zip(new_emails, tree.predict(new_emails)):
        label = "SPAM" if pred == 1 else "ham"
        print(f"[+] e-mail with features {email.tolist()} -> {label}")
    print()


def main() -> None:
    """Run both supervised-learning examples."""
    regression_example()
    classification_example()


if __name__ == "__main__":
    main()
