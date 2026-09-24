#! /usr/bin/env python3
"""
01_string_methods_and_formatting.py
-----------------------------------
Module 3 - Strings, string built-in methods and string formatting.

Covers:
  * creating strings (quotes, triple quotes, raw strings, escapes)
  * indexing, slicing, immutability, concatenation, repetition
  * the most useful built-in string methods (grouped by purpose)
  * formatting with str.format() (positional, keyword, alignment,
    number formats), f-strings and the old % style for comparison

Run:  python 01_string_methods_and_formatting.py
"""


# ---------------------------------------------------------------
# 1. String basics
# ---------------------------------------------------------------
def string_basics() -> None:
    """Creation, indexing, slicing and immutability."""
    print("=== 1. String basics ===")
    single = 'single quotes'
    double = "double quotes"
    multi = """triple quotes
can span lines"""
    raw = r"C:\new\folder"          # raw string: backslashes are literal
    print(single, "|", double)
    print(multi)
    print("raw string   ->", raw)
    print("escape chars -> Tab:\tNewline follows\\n")

    word = "Python"
    print("word[0], word[-1] ->", word[0], word[-1])
    print("word[1:4]         ->", word[1:4])
    print("word[::-1]        ->", word[::-1])
    print("len(word)         ->", len(word))
    print("concat / repeat   ->", word + "3", "|", "ha" * 3)
    print("'th' in word      ->", "th" in word)
    try:
        word[0] = "J"               # strings are immutable
    except TypeError as err:
        print("word[0] = 'J'     -> TypeError:", err)
    print("new string instead->", "J" + word[1:])
    print()


# ---------------------------------------------------------------
# 2. String built-in methods
# ---------------------------------------------------------------
def string_methods() -> None:
    """Tour of string methods grouped by what they do."""
    print("=== 2. String methods ===")
    text = "  machine Learning is FUN  "

    print("-- case --")
    print("upper()      ->", text.upper())
    print("lower()      ->", text.lower())
    print("title()      ->", text.title())
    print("capitalize() ->", text.strip().capitalize())
    print("swapcase()   ->", text.swapcase())
    print("casefold()   ->", "STRASSE".casefold())

    print("-- whitespace --")
    print("strip()  ->", repr(text.strip()))
    print("lstrip() ->", repr(text.lstrip()))
    print("rstrip() ->", repr(text.rstrip()))

    clean = text.strip()
    print("-- search --")
    print("find('is')        ->", clean.find("is"))
    print("find('xyz')       ->", clean.find("xyz"), "(-1 = not found)")
    print("index('FUN')      ->", clean.index("FUN"))
    print("rfind('n')        ->", clean.rfind("n"))
    print("count('n')        ->", clean.count("n"))
    print("startswith('mac') ->", clean.startswith("mac"))
    print("endswith('FUN')   ->", clean.endswith("FUN"))

    print("-- split / join / replace --")
    words = clean.split()
    print("split()           ->", words)
    print("'-'.join(words)   ->", "-".join(words))
    print("split(',', 1)     ->", "a,b,c".split(",", 1))
    print("splitlines()      ->", "line1\nline2".splitlines())
    print("partition(' is ') ->", clean.partition(" is "))
    print("replace()         ->", clean.replace("FUN", "awesome"))

    print("-- checks (return bool) --")
    for sample in ["abc", "123", "abc123", "   ", "Title Case"]:
        print(f"{sample!r:13} isalpha={sample.isalpha()!s:5} isdigit={sample.isdigit()!s:5} "
              f"isalnum={sample.isalnum()!s:5} isspace={sample.isspace()!s:5} istitle={sample.istitle()}")

    print("-- alignment / padding --")
    print(repr("ML".center(10, "*")))
    print(repr("ML".ljust(6, ".")), repr("ML".rjust(6, ".")))
    print("'7'.zfill(3) ->", "7".zfill(3))
    print()


# ---------------------------------------------------------------
# 3. String formatting
# ---------------------------------------------------------------
def string_formatting() -> None:
    """str.format() in depth, plus f-strings and % formatting."""
    print("=== 3. String formatting ===")
    name, age, score = "Alice", 30, 93.4567

    # --- str.format() ---
    print("My name is {} and I am {} years old.".format(name, age))       # positional
    print("{1} is the age of {0}.".format(name, age))                     # by index
    print("{n} scored {s}".format(n=name, s=score))                       # keyword
    person = {"n": "Bob", "a": 25}
    print("{n} is {a}".format(**person))                                  # unpack dict
    print("2 decimals : {:.2f}".format(score))
    print("percentage : {:.1%}".format(0.8765))
    print("thousands  : {:,}".format(1234567))
    print("left  |{:<10}|".format("hi"))
    print("right |{:>10}|".format("hi"))
    print("centre|{:^10}|".format("hi"))
    print("padded: {:05d}".format(42))
    print("binary/hex/octal: {0:b} {0:x} {0:o}".format(255))

    # A small table using format specifiers
    rows = [("Apple", 3, 0.5), ("Banana", 12, 0.25), ("Cherry", 100, 0.1)]
    print("{:<8}{:>6}{:>8}".format("Item", "Qty", "Price"))
    for item, qty, price in rows:
        print("{:<8}{:>6}{:>8.2f}".format(item, qty, price))

    # --- f-strings (Python 3.6+) use the same mini-language ---
    print(f"f-string   : {name} will be {age + 1} next year, score={score:.1f}")
    print(f"debug form : {age=}")
    # --- old %-style (still seen in legacy code) ---
    print("%%-style    : %s is %d years old" % (name, age))
    print()


def main() -> None:
    """Run all demos."""
    string_basics()
    string_methods()
    string_formatting()


if __name__ == "__main__":
    main()
