"""
Module 1 · Script 08 – Random Numbers & Generating Numbers in a Range
=====================================================================

Covers: the modern Generator API (np.random.default_rng), seeds for
reproducibility, random integers/floats in a range, normal distribution,
choice, shuffle, permutation, plus the legacy np.random.* functions.
"""

import numpy as np


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def seeding() -> None:
    """Same seed -> same 'random' numbers (reproducible experiments)."""
    section("1️⃣  Seeds make randomness reproducible")
    rng1 = np.random.default_rng(seed=42)
    rng2 = np.random.default_rng(seed=42)
    print("rng1.random(3):", rng1.random(3).round(4))
    print("rng2.random(3):", rng2.random(3).round(4), "<- identical")


def in_a_range(rng: np.random.Generator) -> None:
    """Generate numbers between a low and high value."""
    section("2️⃣  Numbers between a range")
    print("5 floats in [0, 1)          :", rng.random(5).round(3))
    print("5 floats in [10, 20)        :", rng.uniform(10, 20, size=5).round(2))
    print("5 ints in [1, 7) (dice)     :", rng.integers(1, 7, size=5))
    print("ints in [1, 6] endpoint=True:", rng.integers(1, 6, size=5, endpoint=True))
    print("3x3 ints in [0, 100):\n", rng.integers(0, 100, size=(3, 3)))
    print("Evenly spaced (not random!) :", np.linspace(0, 100, 5))


def distributions(rng: np.random.Generator) -> None:
    """Draw samples from common probability distributions."""
    section("3️⃣  Distributions")
    normal = rng.normal(loc=170, scale=10, size=1000)  # heights in cm
    print(f"normal(170, 10) x1000 -> mean {normal.mean():.1f}, std {normal.std():.1f}")
    print("standard_normal(4)    :", rng.standard_normal(4).round(3))
    print("binomial(10, 0.5, 5)  :", rng.binomial(n=10, p=0.5, size=5), "(heads in 10 flips)")
    print("poisson(3, 5)         :", rng.poisson(lam=3, size=5))


def sampling(rng: np.random.Generator) -> None:
    """Pick, shuffle and permute."""
    section("4️⃣  choice, shuffle, permutation")
    fruits = np.array(["apple", "banana", "cherry", "mango", "kiwi"])
    print("choice 3 (with replacement)   :", rng.choice(fruits, size=3))
    print("choice 3 (no replacement)     :", rng.choice(fruits, size=3, replace=False))
    print("weighted choice               :",
          rng.choice(["win", "lose"], size=6, p=[0.2, 0.8]))
    deck = np.arange(1, 11)
    rng.shuffle(deck)  # in place
    print("shuffled 1..10 (in place)     :", deck)
    print("permutation (returns new)     :", rng.permutation(5))


def legacy_api() -> None:
    """The older np.random.* functions you will still see in tutorials."""
    section("5️⃣  Legacy API (still common in older code)")
    np.random.seed(0)
    print("np.random.rand(3)         :", np.random.rand(3).round(3))
    print("np.random.randn(3)        :", np.random.randn(3).round(3))
    print("np.random.randint(1, 10, 5):", np.random.randint(1, 10, 5))
    print("Prefer np.random.default_rng() in new code.")


if __name__ == "__main__":
    seeding()
    generator = np.random.default_rng(seed=7)
    in_a_range(generator)
    distributions(generator)
    sampling(generator)
    legacy_api()
