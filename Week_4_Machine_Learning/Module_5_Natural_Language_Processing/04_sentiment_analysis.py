"""
04_sentiment_analysis.py
========================
Week 4 · Module 5 – Sentiment Analysis

Two approaches:

  A. LEXICON-BASED (no training): add up the polarity of known words, handle
     negation ("not good"), intensifiers ("very good") and "!!!".
     → NLTK's VADER if installed, otherwise the small fallback in nlp_utils.py.

  B. MACHINE LEARNING: learn from labelled examples.
     clean text → TF-IDF → Logistic Regression / Multinomial Naive Bayes
     evaluated with 5-fold cross-validation on data/reviews.csv (140 reviews).

Run:
    python 04_sentiment_analysis.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from nlp_utils import clean_text, sentiment_backend, sentiment_scores

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "reviews.csv"

EXAMPLES = [
    "I love this phone, the camera is amazing!",
    "The phone is good.",
    "The phone is not good.",
    "The phone is VERY good!!!",
    "Worst purchase ever, totally broken.",
    "It arrived on Tuesday.",
]


def label_from_compound(compound: float) -> str:
    """VADER's standard thresholds."""
    if compound >= 0.05:
        return "positive"
    if compound <= -0.05:
        return "negative"
    return "neutral"


def lexicon_demo(df: pd.DataFrame) -> None:
    """Score example sentences and the whole dataset with the lexicon approach."""
    print("=" * 70)
    print(f"A. Lexicon-based sentiment  (engine: {sentiment_backend()})")
    print("=" * 70)
    for text in EXAMPLES:
        c = sentiment_scores(text)["compound"]
        print(f"    {c:+.3f} {label_from_compound(c):<9} | {text}")
    preds = [label_from_compound(sentiment_scores(t)["compound"]) for t in df["review"]]
    acc = np.mean(np.array(preds) == df["sentiment"].to_numpy())
    print(f"\n[*] Lexicon accuracy on the {len(df)} labelled reviews: {acc:.3f}"
          "  ('neutral' counts as wrong)")


def ml_demo(df: pd.DataFrame) -> None:
    """Train TF-IDF + classifier models and evaluate with cross-validation."""
    # Lesson learned while building this: with only the first 60 (very varied)
    # reviews, CV accuracy was BELOW 50 % – the models had too few repeated
    # sentiment words to learn from. More data fixed it. Data > algorithms!
    print("\n" + "=" * 70)
    print("B. Machine-learning sentiment (TF-IDF + classifier, 5-fold CV)")
    print("=" * 70)
    X = df["review"].apply(clean_text)
    y = df["sentiment"]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Multinomial Naive Bayes": MultinomialNB(),
    }
    for name, clf in models.items():
        pipe = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), clf)
        preds = cross_val_predict(pipe, X, y, cv=cv)
        print(f"[+] {name:<25} CV accuracy = {accuracy_score(y, preds):.3f}")

    # Fit on all data to inspect the most telling words and predict new text
    pipe = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000)).fit(X, y)
    vec, clf = pipe.named_steps["tfidfvectorizer"], pipe.named_steps["logisticregression"]
    words = vec.get_feature_names_out()
    order = np.argsort(clf.coef_[0])
    print(f"\n[*] Most NEGATIVE words: {list(words[order[:8]])}")
    print(f"[*] Most POSITIVE words: {list(words[order[-8:][::-1]])}")
    new = ["The quality is excellent and delivery was fast",
           "It broke after one day, terrible"]
    for text, pred in zip(new, pipe.predict([clean_text(t) for t in new])):
        print(f"    → {pred:<8} | {text}")
    print(f"\n[*] Note: {len(df)} reviews is a TINY dataset – real systems train on thousands.")


def main() -> None:
    """Run both sentiment approaches."""
    df = pd.read_csv(DATA_PATH)
    print(f"[*] Loaded {len(df)} reviews: {df['sentiment'].value_counts().to_dict()}\n")
    lexicon_demo(df)
    ml_demo(df)


if __name__ == "__main__":
    main()
