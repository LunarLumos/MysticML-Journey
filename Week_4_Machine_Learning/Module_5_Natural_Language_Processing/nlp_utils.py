"""
nlp_utils.py
============
Shared helpers for Week 4 · Module 5 (NLP).

NLTK needs extra DATA packages (tokenizer models, stop-word lists, WordNet,
VADER lexicon, NER chunker ...) that are downloaded separately with
`python download_nltk_data.py`. Those downloads need internet.

To keep every script runnable OFFLINE, each helper here:
    1. uses the NLTK resource if it is installed, otherwise
    2. falls back to a small, clearly-labelled rule-based version.

Set the environment variable  NLP_FORCE_FALLBACK=1  to force the fallbacks
(handy to see how the simple versions behave, and for testing).
"""

from __future__ import annotations

import os
import re
import string

FORCE_FALLBACK = os.environ.get("NLP_FORCE_FALLBACK") == "1"

# ---------------------------------------------------------------
# Resource detection
# ---------------------------------------------------------------
_RESOURCE_PATHS = {
    "punkt_tab": "tokenizers/punkt_tab/english/",
    "stopwords": "corpora/stopwords",
    "wordnet": "corpora/wordnet",
    "omw-1.4": "corpora/omw-1.4",
    "vader_lexicon": "sentiment/vader_lexicon.zip",
    "averaged_perceptron_tagger_eng": "taggers/averaged_perceptron_tagger_eng/",
    "maxent_ne_chunker_tab": "chunkers/maxent_ne_chunker_tab/english_ace_multiclass/",
    "words": "corpora/words",
}
_cache: dict[str, bool] = {}


def has_nltk_resource(name: str) -> bool:
    """Return True if the NLTK data package `name` is installed (and not forced off)."""
    if FORCE_FALLBACK:
        return False
    if name not in _cache:
        try:
            import nltk
            nltk.data.find(_RESOURCE_PATHS[name])
            _cache[name] = True
        except (LookupError, ImportError, OSError):
            _cache[name] = False
    return _cache[name]


def backend_report() -> str:
    """One line per resource saying whether NLTK or the fallback is used."""
    lines = []
    for name in _RESOURCE_PATHS:
        lines.append(f"    {name:<32} {'NLTK ✔' if has_nltk_resource(name) else 'fallback'}")
    return "\n".join(lines)


# ---------------------------------------------------------------
# Tokenisation
# ---------------------------------------------------------------
_TOKEN_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:\.\d+)?|[^\w\s]")


def tokenize(text: str) -> list[str]:
    """Split text into word tokens (NLTK word_tokenize or a regex fallback)."""
    if has_nltk_resource("punkt_tab"):
        from nltk.tokenize import word_tokenize
        return word_tokenize(text)
    return _TOKEN_RE.findall(text)


def sent_tokenize(text: str) -> list[str]:
    """Split text into sentences (NLTK Punkt or a regex fallback)."""
    if has_nltk_resource("punkt_tab"):
        from nltk.tokenize import sent_tokenize as nltk_sent
        return nltk_sent(text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


# ---------------------------------------------------------------
# Stop words
# ---------------------------------------------------------------
_FALLBACK_STOPWORDS = set("""
a about above after again against all am an and any are as at be because been before
being below between both but by can could did do does doing down during each few for
from further had has have having he her here hers herself him himself his how i if in
into is it its itself just me more most my myself no nor not now of off on once only or
other our ours ourselves out over own same she should so some such than that the their
theirs them themselves then there these they this those through to too under until up
very was we were what when where which while who whom why will with would you your
yours yourself yourselves
""".split())


def get_stopwords() -> set[str]:
    """English stop words from NLTK, or a built-in list."""
    if has_nltk_resource("stopwords"):
        from nltk.corpus import stopwords
        return set(stopwords.words("english"))
    return set(_FALLBACK_STOPWORDS)


# ---------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------
CONTRACTIONS = {
    "won't": "will not", "can't": "cannot", "n't": " not", "'re": " are",
    "'s": " is", "'d": " would", "'ll": " will", "'ve": " have", "'m": " am",
}


def expand_contractions(text: str) -> str:
    """don't → do not, I'm → I am, ... (simple rule-based)."""
    for short, full in CONTRACTIONS.items():
        text = text.replace(short, full)
    return text


def clean_text(text: str, remove_stopwords: bool = True,
               keep_negations: bool = True) -> str:
    """A typical cleaning pipeline; returns a cleaned, space-joined string."""
    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)                    # HTML tags
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)      # URLs
    text = re.sub(r"\S+@\S+", " ", text)                    # e-mails
    text = expand_contractions(text)
    text = re.sub(r"\d+", " ", text)                        # numbers
    text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    text = text.encode("ascii", "ignore").decode()          # emojis / non-ascii
    tokens = text.split()
    if remove_stopwords:
        stops = get_stopwords()
        if keep_negations:  # "not good" ≠ "good" – keep negations for sentiment!
            stops -= {"not", "no", "nor", "cannot"}
        tokens = [t for t in tokens if t not in stops and len(t) > 1]
    return " ".join(tokens)


# ---------------------------------------------------------------
# Lemmatisation
# ---------------------------------------------------------------
_IRREGULAR = {
    "was": "be", "were": "be", "is": "be", "are": "be", "am": "be", "been": "be",
    "has": "have", "had": "have", "did": "do", "does": "do", "done": "do",
    "went": "go", "gone": "go", "ran": "run", "running": "run", "better": "good",
    "best": "good", "worse": "bad", "worst": "bad", "mice": "mouse", "geese": "goose",
    "children": "child", "feet": "foot", "teeth": "tooth", "men": "man", "women": "woman",
    "people": "person", "studies": "study", "studying": "study", "ate": "eat", "eaten": "eat",
    "flies": "fly", "flew": "fly", "saw": "see", "wrote": "write", "written": "write", "bought": "buy", "caring": "care",
}


def _fallback_lemma(word: str, pos: str) -> str:
    """Very small rule-based lemmatiser (dictionary + suffix rules)."""
    w = word.lower()
    if w in _IRREGULAR and (pos in ("v", "a") or w in ("mice", "geese", "children", "feet",
                                                        "teeth", "men", "women", "people")):
        return _IRREGULAR[w]
    if pos == "n":
        if w.endswith("ies") and len(w) > 4:
            return w[:-3] + "y"
        if w.endswith(("ches", "shes", "xes", "sses")):
            return w[:-2]
        if w.endswith("s") and not w.endswith("ss") and len(w) > 3:
            return w[:-1]
    if pos == "v":
        for suffix in ("ing", "ed"):
            if w.endswith(suffix) and len(w) > len(suffix) + 2:
                stem = w[: -len(suffix)]
                if len(stem) > 2 and stem[-1] == stem[-2]:      # running → run
                    stem = stem[:-1]
                return stem
        if w.endswith("ies"):
            return w[:-3] + "y"
        if w.endswith("es") and w[-3] in "sxz":
            return w[:-2]
        if w.endswith("s") and not w.endswith("ss"):
            return w[:-1]
    return w


def lemmatize(word: str, pos: str = "n") -> str:
    """Lemmatise a word. pos: 'n' noun, 'v' verb, 'a' adjective, 'r' adverb."""
    if has_nltk_resource("wordnet"):
        from nltk.stem import WordNetLemmatizer
        return WordNetLemmatizer().lemmatize(word.lower(), pos=pos)
    return _fallback_lemma(word, pos)


# ---------------------------------------------------------------
# Sentiment (lexicon based)
# ---------------------------------------------------------------
_POS_WORDS = {"good": 1.9, "great": 3.1, "excellent": 3.2, "amazing": 2.8, "love": 3.2,
              "loved": 2.9, "happy": 2.7, "fantastic": 2.6, "perfect": 2.7, "nice": 1.8,
              "wonderful": 2.7, "best": 3.2, "awesome": 3.1, "fast": 1.0, "recommend": 1.5,
              "comfortable": 1.8, "beautiful": 2.9, "easy": 1.9, "helpful": 1.8, "like": 1.5,
              "enjoy": 2.2, "enjoyed": 2.3, "works": 1.0, "worth": 1.2, "friendly": 2.2}
_NEG_WORDS = {"bad": -2.5, "terrible": -2.1, "awful": -2.0, "hate": -2.7, "poor": -2.1,
              "worst": -3.1, "broken": -1.9, "broke": -1.8, "slow": -1.0, "disappointed": -2.1,
              "disappointing": -2.2, "waste": -1.8, "useless": -1.8, "horrible": -2.5,
              "rude": -2.0, "cheap": -1.0, "refund": -1.0, "problem": -1.7, "boring": -1.3,
              "sad": -2.1, "angry": -2.3, "never": -0.5, "fail": -2.3, "failed": -2.3}
_NEGATIONS = {"not", "no", "never", "n't", "cannot", "dont", "don't", "isn't", "wasn't"}
_BOOSTERS = {"very": 0.3, "really": 0.3, "extremely": 0.5, "so": 0.2, "super": 0.4}


def _fallback_sentiment(text: str) -> dict[str, float]:
    """Tiny VADER-like scorer: word scores, negation flip, boosters, '!' emphasis."""
    tokens = [t.lower() for t in _TOKEN_RE.findall(text)]
    score = 0.0
    for i, tok in enumerate(tokens):
        value = _POS_WORDS.get(tok, 0.0) + _NEG_WORDS.get(tok, 0.0)
        if not value:
            continue
        window = tokens[max(0, i - 3):i]
        if any(w in _BOOSTERS for w in window):
            value *= 1 + max(_BOOSTERS.get(w, 0) for w in window)
        if any(w in _NEGATIONS for w in window):
            value *= -0.74                      # VADER's negation constant
        score += value
    score += 0.3 * min(text.count("!"), 3) * (1 if score >= 0 else -1) if score else 0
    compound = score / (score ** 2 + 15) ** 0.5  # VADER's normalisation to −1..1
    return {"compound": round(compound, 4)}


def sentiment_scores(text: str) -> dict[str, float]:
    """Return a dict with at least 'compound' in [−1, 1] (VADER or fallback)."""
    if has_nltk_resource("vader_lexicon"):
        from nltk.sentiment import SentimentIntensityAnalyzer
        return SentimentIntensityAnalyzer().polarity_scores(text)
    return _fallback_sentiment(text)


def sentiment_backend() -> str:
    """Name of the sentiment engine in use."""
    return "NLTK VADER" if has_nltk_resource("vader_lexicon") else "rule-based fallback"
