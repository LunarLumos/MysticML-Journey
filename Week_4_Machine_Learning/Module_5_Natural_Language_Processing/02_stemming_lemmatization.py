"""
02_stemming_lemmatization.py
============================
Week 4 · Module 5 – Concept of Stemming & Lemmatization

Both reduce words to a base form so "run", "runs", "running" count as ONE feature.

  STEMMING       – chops suffixes with rules. Fast, crude, may produce non-words.
                   studies → studi,   running → run,   better → better
  LEMMATIZATION  – looks the word up in a dictionary (WordNet) using its part of
                   speech. Slower, but returns real words.
                   studies → study,   running (verb) → run,   better (adj) → good

Stemmers (Porter, Lancaster, Snowball) ship with NLTK's code – no download needed.
The WordNet lemmatiser needs the 'wordnet' data package → fallback otherwise.

Run:
    python 02_stemming_lemmatization.py
"""

from nltk.stem import LancasterStemmer, PorterStemmer, SnowballStemmer

from nlp_utils import clean_text, has_nltk_resource, lemmatize, tokenize

WORDS = [("running", "v"), ("ran", "v"), ("runs", "v"), ("studies", "n"),
         ("studying", "v"), ("better", "a"), ("mice", "n"), ("feet", "n"),
         ("happily", "r"), ("caring", "v"), ("organization", "n"), ("generously", "r")]


def compare_table() -> None:
    """Print stemmers vs lemmatiser side by side."""
    porter, lancaster = PorterStemmer(), LancasterStemmer()
    snowball = SnowballStemmer("english")
    engine = "WordNet" if has_nltk_resource("wordnet") else "rule-based fallback"
    print(f"[*] Lemmatiser in use: {engine}\n")
    print(f"{'word':<14}{'POS':<5}{'Porter':<12}{'Lancaster':<12}{'Snowball':<12}{'Lemma'}")
    print("-" * 66)
    for word, pos in WORDS:
        print(f"{word:<14}{pos:<5}{porter.stem(word):<12}{lancaster.stem(word):<12}"
              f"{snowball.stem(word):<12}{lemmatize(word, pos)}")


def pos_matters() -> None:
    """The same word gives different lemmas depending on its part of speech."""
    print("\n[*] Why POS matters for lemmatisation:")
    for word in ("meeting", "better", "saw"):
        forms = {pos: lemmatize(word, pos) for pos in ("n", "v", "a")}
        print(f"    {word:<8} noun→{forms['n']:<8} verb→{forms['v']:<8} adj→{forms['a']}")


def on_a_sentence() -> None:
    """Apply stemming and lemmatisation to a cleaned sentence."""
    sentence = "The children were running and studying while the geese flew over the houses"
    tokens = tokenize(clean_text(sentence, remove_stopwords=True))
    porter = PorterStemmer()
    print(f"\n[*] Sentence: {sentence}")
    print(f"    tokens     : {tokens}")
    print(f"    stemmed    : {[porter.stem(t) for t in tokens]}")
    print(f"    lemmatised : {[lemmatize(t, 'v' if t.endswith('ing') else 'n') for t in tokens]}")


def main() -> None:
    """Run all comparisons."""
    compare_table()
    pos_matters()
    on_a_sentence()
    print("\n[*] Rule of thumb: stemming for speed (search engines), "
          "lemmatisation when readable words matter (chatbots, analysis).")


if __name__ == "__main__":
    main()
