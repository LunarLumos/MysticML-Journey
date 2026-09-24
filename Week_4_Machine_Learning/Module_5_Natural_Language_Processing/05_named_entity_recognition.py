"""
05_named_entity_recognition.py
==============================
Week 4 · Module 5 – (Named) Entity Recognition

NER finds the "things" in text and labels them:
    PERSON, ORGANIZATION, GPE (countries/cities), DATE, MONEY, ...

Engines, in order of preference:
  1. NLTK  : word_tokenize → pos_tag → ne_chunk   (needs punkt_tab,
             averaged_perceptron_tagger_eng, maxent_ne_chunker_tab, words)
  2. Fallback (always available): REGEX rules for dates / money / e-mails /
     percentages + a small GAZETTEER (lookup list) + "Capitalised Word
     Sequence" heuristic for unknown proper nouns.

Run:
    python 05_named_entity_recognition.py
"""

import re

from nlp_utils import has_nltk_resource

TEXTS = [
    "Sundar Pichai announced on 12 March 2024 that Google will invest $2 billion in India.",
    "Marie Curie moved from Warsaw to Paris and later worked at the University of Paris.",
    "Contact Aisha Khan at aisha.khan@example.org before Friday; Microsoft shares rose 3.5%.",
]

# ---------------------------------------------------------------
# Fallback: regex + gazetteer
# ---------------------------------------------------------------
GAZETTEER = {
    "GPE": {"India", "Pakistan", "Paris", "Warsaw", "London", "France", "Poland",
            "Karachi", "New York", "China", "Germany", "United States"},
    "ORGANIZATION": {"Google", "Microsoft", "Apple", "Amazon", "NASA", "OpenAI",
                     "University of Paris", "United Nations"},
}
MONTHS = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|" \
         r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
REGEX_RULES = [
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b")),
    ("MONEY", re.compile(r"[$€£]\s?\d[\d,.]*(?:\s(?:million|billion|thousand))?")),
    ("PERCENT", re.compile(r"\b\d+(?:\.\d+)?%")),
    ("DATE", re.compile(rf"\b\d{{1,2}}\s{MONTHS}\s\d{{4}}\b|\b{MONTHS}\s\d{{1,2}},?\s\d{{4}}\b|"
                        r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b")),
]
SENTENCE_STARTERS = {"The", "A", "An", "Contact", "On", "In", "He", "She", "It", "They"}


def regex_ner(text: str) -> list[tuple[str, str]]:
    """Rule-based NER fallback. Returns a list of (entity text, label)."""
    entities, taken = [], []

    def add(start: int, end: int, label: str) -> None:
        if not any(s < end and start < e for s, e in taken):  # avoid overlaps
            taken.append((start, end))
            entities.append((start, text[start:end], label))

    for label, pattern in REGEX_RULES:
        for m in pattern.finditer(text):
            add(m.start(), m.end(), label)
    lookup = [(name, label) for label, names in GAZETTEER.items() for name in names]
    for name, label in sorted(lookup, key=lambda x: len(x[0]), reverse=True):
        # longest names first, so "University of Paris" wins over "Paris"
        for m in re.finditer(rf"\b{re.escape(name)}\b", text):
            add(m.start(), m.end(), label)
    # Unknown capitalised sequences of 2+ words → probably a PERSON
    for m in re.finditer(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b", text):
        start, words = m.start(), m.group().split()
        if words[0] in SENTENCE_STARTERS:          # "Contact Aisha Khan" → "Aisha Khan"
            start += len(words[0]) + 1
            words = words[1:]
        if len(words) >= 2:
            add(start, m.end(), "PERSON")
    return [(ent, label) for _, ent, label in sorted(entities)]


# ---------------------------------------------------------------
# NLTK engine
# ---------------------------------------------------------------
def nltk_available() -> bool:
    """True if all NLTK resources for ne_chunk are installed."""
    return all(has_nltk_resource(r) for r in ("punkt_tab", "averaged_perceptron_tagger_eng",
                                              "maxent_ne_chunker_tab", "words"))


def nltk_ner(text: str) -> list[tuple[str, str]]:
    """NER with NLTK's pre-trained MaxEnt chunker."""
    import nltk
    tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))
    return [(" ".join(tok for tok, _ in subtree.leaves()), subtree.label())
            for subtree in tree if hasattr(subtree, "label")]


def main() -> None:
    """Run NER on sample sentences with the best available engine(s)."""
    use_nltk = nltk_available()
    print(f"[*] NLTK NER available: {use_nltk}  (fallback regex NER is always shown)\n")
    for text in TEXTS:
        print(f"TEXT: {text}")
        if use_nltk:
            print(f"  NLTK  : {nltk_ner(text)}")
            import nltk
            print(f"  POS   : {nltk.pos_tag(nltk.word_tokenize(text))[:6]} ...")
        print(f"  Regex : {regex_ner(text)}\n")
    print("[*] Note: NLTK's chunker does not detect DATE/MONEY; the regex rules do.")
    print("    Production systems use spaCy or transformer models for higher accuracy.")


if __name__ == "__main__":
    main()
