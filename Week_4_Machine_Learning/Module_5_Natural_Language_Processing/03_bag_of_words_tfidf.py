"""
03_bag_of_words_tfidf.py
========================
Week 4 · Module 5 – Bag of Words & TF-IDF

BAG OF WORDS (BoW): represent a document by COUNTING each vocabulary word.
    Word order is lost ("dog bites man" == "man bites dog") but it works well!

TF-IDF re-weights the counts so words that appear in EVERY document (like
"the", "movie") matter less and rare, distinctive words matter more:

    tf(t, d)   = count of term t in document d
    idf(t)     = ln( (1 + N) / (1 + df(t)) ) + 1        (scikit-learn's smooth idf)
    tfidf(t,d) = tf(t, d) · idf(t)      → then each row is L2-normalised

We build both BY HAND and check against scikit-learn, then use TF-IDF with
cosine similarity to find similar documents.

Run:
    python 03_bag_of_words_tfidf.py
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CORPUS = [
    "the movie was good and the acting was good",
    "the movie was bad",
    "the acting was great and the story was great",
    "a bad story and bad acting",
]


def manual_bow(docs: list[str]) -> tuple[list[str], np.ndarray]:
    """Return (vocabulary, count matrix) built with plain Python."""
    vocab = sorted({w for d in docs for w in d.split()})
    index = {w: i for i, w in enumerate(vocab)}
    matrix = np.zeros((len(docs), len(vocab)), dtype=int)
    for row, doc in enumerate(docs):
        for word in doc.split():
            matrix[row, index[word]] += 1
    return vocab, matrix


def manual_tfidf(counts: np.ndarray) -> np.ndarray:
    """TF-IDF exactly as scikit-learn computes it (smooth idf + L2 norm)."""
    n_docs = counts.shape[0]
    df = np.count_nonzero(counts, axis=0)
    idf = np.log((1 + n_docs) / (1 + df)) + 1
    tfidf = counts * idf
    return tfidf / np.linalg.norm(tfidf, axis=1, keepdims=True)


def main() -> None:
    """Build BoW/TF-IDF manually and with sklearn, then do similarity search."""
    vocab, counts = manual_bow(CORPUS)
    print("=" * 70)
    print("Bag of Words (manual)")
    print("=" * 70)
    print(pd.DataFrame(counts, columns=vocab, index=[f"doc{i}" for i in range(len(CORPUS))]))

    cv = CountVectorizer(token_pattern=r"(?u)\b\w+\b")  # keep 1-letter words like "a"
    sk_counts = cv.fit_transform(CORPUS).toarray()
    print(f"\n[*] Same as sklearn CountVectorizer? {np.array_equal(counts, sk_counts)}")

    tfidf = manual_tfidf(counts)
    sk_tfidf = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b").fit_transform(CORPUS).toarray()
    print("\n" + "=" * 70)
    print("TF-IDF (manual) – note 'the'/'was' get LOW weights, 'good'/'great' HIGH")
    print("=" * 70)
    print(pd.DataFrame(tfidf, columns=vocab).round(2))
    print(f"\n[*] Same as sklearn TfidfVectorizer? {np.allclose(tfidf, sk_tfidf)}")

    # --- N-grams keep a little word order ---
    bigrams = CountVectorizer(ngram_range=(1, 2), stop_words="english").fit(CORPUS)
    print(f"\n[*] Uni+bi-gram features (stop words removed): "
          f"{list(bigrams.get_feature_names_out())}")

    # --- Similarity search ---
    vec = TfidfVectorizer()
    X = vec.fit_transform(CORPUS)
    query = "great acting in this movie"
    sims = cosine_similarity(vec.transform([query]), X).ravel()
    print(f"\n[*] Query: '{query}'  → cosine similarity to each document:")
    for i in np.argsort(sims)[::-1]:
        print(f"    {sims[i]:.3f}  {CORPUS[i]}")


if __name__ == "__main__":
    main()
