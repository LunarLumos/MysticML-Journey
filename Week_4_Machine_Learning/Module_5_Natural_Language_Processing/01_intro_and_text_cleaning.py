"""
01_intro_and_text_cleaning.py
=============================
Week 4 · Module 5 – Introduction to NLP & Text Cleaning in Python

Natural Language Processing (NLP) turns human language into numbers a model
can learn from. A classic NLP pipeline:

    raw text → clean → tokenise → normalise (stem / lemmatise)
             → vectorise (BoW / TF-IDF) → model (classifier, clustering ...)

This script walks through every CLEANING step on a messy example, then applies
the full cleaner to data/reviews.csv.

Run:
    python 01_intro_and_text_cleaning.py
"""

import re
import string
from collections import Counter
from pathlib import Path

import pandas as pd

from nlp_utils import (backend_report, clean_text, expand_contractions, get_stopwords,
                       sent_tokenize, tokenize)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "reviews.csv"

MESSY = ("<p>OMG!!! I can't believe it 😍 — the NEW phone arrived in 2 days.</p> "
         "Check https://example.com/deal or mail me at fan@example.com. "
         "Honestly, it's the BEST phone I've had!!!")


def step_by_step(text: str) -> None:
    """Show the effect of each cleaning step in order."""
    print("=" * 70)
    print("Text cleaning, one step at a time")
    print("=" * 70)
    print(f"[0] raw             : {text}")
    text = text.lower()
    print(f"[1] lowercase       : {text}")
    text = re.sub(r"<[^>]+>", " ", text)
    print(f"[2] strip HTML      : {text}")
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    print(f"[3] URLs & e-mails  : {text}")
    text = expand_contractions(text)
    print(f"[4] contractions    : {text}")
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    text = text.encode("ascii", "ignore").decode()
    text = re.sub(r"\s+", " ", text).strip()
    print(f"[5] digits/punct/emoji removed: {text}")
    tokens = text.split()
    print(f"[6] tokens ({len(tokens)})     : {tokens}")
    stops = get_stopwords() - {"not", "no"}
    kept = [t for t in tokens if t not in stops]
    print(f"[7] stop words removed ({len(kept)}): {kept}")


def main() -> None:
    """Demonstrate cleaning and apply it to the reviews dataset."""
    print("[*] Which NLTK resources are available (else fallback is used):")
    print(backend_report())
    print()

    print("[*] Sentence tokenisation:")
    for s in sent_tokenize("NLP is fun. It powers chatbots! Does it translate too? Yes."):
        print(f"    • {s}")
    sample = "Don't panic: NLP isn't magic, it's maths!"
    print(f"[*] Word tokenisation: {tokenize(sample)}\n")

    step_by_step(MESSY)

    df = pd.read_csv(DATA_PATH)
    df["clean"] = df["review"].apply(clean_text)
    print("\n[*] Reviews before → after cleaning:")
    for raw, clean in df[["review", "clean"]].head(4).values:
        print(f"    {raw}\n      → {clean}")

    words = Counter(" ".join(df["clean"]).split())
    print(f"\n[*] Vocabulary size after cleaning: {len(words)} unique words")
    print(f"[*] 10 most frequent words: {words.most_common(10)}")


if __name__ == "__main__":
    main()
