"""
06_nlp_examples.py
==================
Week 4 · Module 5 – Examples: putting the NLP toolbox to work

  Example 1 – SPAM DETECTOR: clean → TF-IDF → Naive Bayes on a small SMS set
  Example 2 – KEYWORD EXTRACTION: top TF-IDF words per document
  Example 3 – FAQ BOT: answer a question by finding the most similar FAQ
              (TF-IDF + cosine similarity) – the core idea behind search engines
  Example 4 – TEXT STATISTICS: word frequencies & lexical diversity of reviews

Run:
    python 06_nlp_examples.py
"""

from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

from nlp_utils import clean_text

BASE_DIR = Path(__file__).resolve().parent
STEMMER = PorterStemmer()

SMS = [
    ("WINNER!! You have won a free cruise, call now to claim your prize", "spam"),
    ("Congratulations! Claim your free iPhone by clicking this link", "spam"),
    ("URGENT: your account is suspended, verify your password here", "spam"),
    ("Get cheap loans instantly, no credit check, reply YES", "spam"),
    ("You have been selected for a cash reward of 5000, text WIN", "spam"),
    ("Limited offer!!! Buy one get three free, visit our site now", "spam"),
    ("Earn money from home fast, guaranteed income, call today", "spam"),
    ("Final notice: claim your lottery prize before midnight", "spam"),
    ("Free entry to win tickets, text CLAIM to 80082", "spam"),
    ("Exclusive deal just for you, click to unlock your free gift", "spam"),
    ("Are we still meeting for lunch tomorrow?", "ham"),
    ("Can you send me the notes from today's class", "ham"),
    ("I'll be home late, don't wait for dinner", "ham"),
    ("Happy birthday! Hope you have a great day", "ham"),
    ("The meeting moved to 3pm, see you in room 12", "ham"),
    ("Did you finish the machine learning assignment?", "ham"),
    ("Mom says call her when you get a chance", "ham"),
    ("Thanks for the help yesterday, really appreciate it", "ham"),
    ("Let's watch the match together on Saturday", "ham"),
    ("Please pick up milk and bread on your way back", "ham"),
]

FAQ = {
    "How do I reset my password?": "Go to Settings → Security → Reset password.",
    "What is your refund policy?": "Refunds are accepted within 30 days with a receipt.",
    "How long does shipping take?": "Standard shipping takes 3–5 business days.",
    "Can I change my delivery address?": "Yes, before the order ships, under My Orders.",
    "Do you ship internationally?": "We ship to over 40 countries worldwide.",
}


def stem_clean(text: str) -> str:
    """Clean + stem, so 'claim', 'claiming' and 'claimed' become one feature."""
    return " ".join(STEMMER.stem(w) for w in clean_text(text).split())


def spam_detector() -> None:
    """Example 1: a tiny spam classifier."""
    print("=" * 70)
    print("Example 1 · Spam detector (TF-IDF + Multinomial Naive Bayes)")
    print("=" * 70)
    texts, labels = zip(*SMS)
    X = [stem_clean(t) for t in texts]
    X_tr, X_te, y_tr, y_te = train_test_split(X, labels, test_size=0.3, stratify=labels,
                                              random_state=1)
    model = make_pipeline(TfidfVectorizer(), MultinomialNB()).fit(X_tr, y_tr)
    print(classification_report(y_te, model.predict(X_te), zero_division=0))
    for msg in ("Claim your FREE prize now!!!", "See you at the library at 5?"):
        print(f"    {model.predict([stem_clean(msg)])[0]:<5} ← {msg}")


def keyword_extraction(df: pd.DataFrame) -> None:
    """Example 2: top TF-IDF keywords of a few reviews."""
    print("\n" + "=" * 70)
    print("Example 2 · Keyword extraction with TF-IDF")
    print("=" * 70)
    docs = df["review"].apply(clean_text)
    vec = TfidfVectorizer()
    X = vec.fit_transform(docs)
    words = vec.get_feature_names_out()
    for i in (0, 14, 31):
        row = X[i].toarray().ravel()
        top = [words[j] for j in np.argsort(row)[::-1][:3] if row[j] > 0]
        print(f"    {top}  ← {df['review'][i]}")


def faq_bot() -> None:
    """Example 3: retrieve the closest FAQ answer."""
    print("\n" + "=" * 70)
    print("Example 3 · FAQ bot with cosine similarity")
    print("=" * 70)
    questions = list(FAQ)
    vec = TfidfVectorizer().fit([stem_clean(q) for q in questions])
    Q = vec.transform([stem_clean(q) for q in questions])
    for user_q in ("I forgot my password", "how long will shipping take to Canada?",
                   "can I get a refund?", "when will my parcel arrive?",
                   "what is the weather today"):
        sims = (vec.transform([stem_clean(user_q)]) @ Q.T).toarray().ravel()
        best = int(np.argmax(sims))
        answer = FAQ[questions[best]] if sims[best] > 0.1 else "Sorry, I don't know that one."
        print(f"    Q: {user_q:<38} (sim={sims[best]:.2f}) → {answer}")
    print("    → 'parcel arrive' shares no WORD with 'shipping take': TF-IDF can't see\n"
          "      synonyms. Word embeddings / transformers (Week 6) solve this.")


def text_statistics(df: pd.DataFrame) -> None:
    """Example 4: simple corpus statistics by sentiment."""
    print("\n" + "=" * 70)
    print("Example 4 · Text statistics by sentiment")
    print("=" * 70)
    for label, group in df.groupby("sentiment"):
        tokens = " ".join(group["review"].apply(clean_text)).split()
        diversity = len(set(tokens)) / len(tokens)
        print(f"    {label:<9} avg words/review={group['review'].str.split().str.len().mean():.1f}"
              f"  lexical diversity={diversity:.2f}  top={Counter(tokens).most_common(4)}")


def main() -> None:
    """Run all examples."""
    df = pd.read_csv(BASE_DIR / "data" / "reviews.csv")
    spam_detector()
    keyword_extraction(df)
    faq_bot()
    text_statistics(df)


if __name__ == "__main__":
    main()
