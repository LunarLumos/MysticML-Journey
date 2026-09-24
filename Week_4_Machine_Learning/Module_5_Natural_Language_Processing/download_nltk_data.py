"""
download_nltk_data.py
=====================
One-time download of the NLTK data packages used in this module (needs internet).

Every other script in this folder still RUNS without these packages – it just
uses simpler rule-based fallbacks (see nlp_utils.py) and tells you so.

Run:
    python download_nltk_data.py                 # default NLTK location (~/nltk_data)
    python download_nltk_data.py --dir ./nltk_data
"""

import argparse

import nltk

PACKAGES = [
    "punkt_tab",                       # tokeniser models
    "stopwords",                       # stop-word lists
    "wordnet", "omw-1.4",              # lemmatiser dictionary
    "vader_lexicon",                   # sentiment lexicon
    "averaged_perceptron_tagger_eng",  # part-of-speech tagger (needed by NER)
    "maxent_ne_chunker_tab",           # named-entity chunker
    "words",                           # word list used by the NE chunker
]


def main() -> None:
    """Download each package and report success/failure."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--dir", default=None, help="download directory")
    args = parser.parse_args()
    ok = 0
    for pkg in PACKAGES:
        try:
            success = nltk.download(pkg, download_dir=args.dir, quiet=True)
        except Exception as exc:  # network errors etc.
            success = False
            print(f"[!] {pkg}: {exc}")
        print(f"[{'+' if success else '!'}] {pkg:<32} {'ok' if success else 'FAILED'}")
        ok += bool(success)
    print(f"\n[*] {ok}/{len(PACKAGES)} packages available.")
    if ok < len(PACKAGES):
        print("    No internet? That's fine – the scripts fall back to rule-based versions.")


if __name__ == "__main__":
    main()
