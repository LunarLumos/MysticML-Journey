"""
Module 3 · Script 05 – .value_counts() and .apply() Methods
===========================================================

value_counts(): how often does each value appear?
apply():        run any Python function on every element.
"""

import pandas as pd


def section(title: str) -> None:
    """Print a pretty section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def value_counts_demo() -> None:
    """All the useful options of value_counts()."""
    orders = pd.Series(["pizza", "burger", "pizza", "pasta", "pizza", "burger",
                        None, "salad", "pasta", "pizza"], name="dish")
    section("1️⃣  value_counts() – frequency table (sorted, NaN dropped)")
    print(orders.value_counts())

    section("2️⃣  normalize=True – proportions instead of counts")
    print((orders.value_counts(normalize=True) * 100).round(1).astype(str) + " %")

    section("3️⃣  dropna=False – also count missing values")
    print(orders.value_counts(dropna=False))

    section("4️⃣  ascending=True & sort=False")
    print("ascending :", orders.value_counts(ascending=True).to_dict())
    print("sort=False:", orders.value_counts(sort=False).to_dict())

    section("5️⃣  bins= for numeric data")
    ages = pd.Series([12, 18, 25, 33, 41, 47, 52, 60, 67, 71])
    print(ages.value_counts(bins=3, sort=False))

    section("6️⃣  Most common value")
    print("Most ordered dish:", orders.value_counts().idxmax())


def grade(mark: float) -> str:
    """Convert a numeric mark to a letter grade."""
    if mark >= 90:
        return "A"
    if mark >= 75:
        return "B"
    if mark >= 60:
        return "C"
    return "F"


def apply_demo() -> None:
    """Using apply() with named functions, lambdas and extra arguments."""
    marks = pd.Series([95, 82, 58, 74, 66], index=["Aadil", "Yaana", "Sama", "Lilith", "Rohan"])

    section("7️⃣  apply() with a named function")
    print(marks.apply(grade))

    section("8️⃣  apply() with a lambda")
    print(marks.apply(lambda m: m + 5 if m < 60 else m).to_dict(), "(grace marks)")

    section("9️⃣  apply() with extra arguments")

    def scale(value: float, factor: float, offset: float = 0) -> float:
        return value * factor + offset

    print(marks.apply(scale, args=(0.1,), offset=1).to_dict())

    section("🔟  apply() on strings & combining with value_counts()")
    names = pd.Series(["aadil", "yaana", "sama", "lilith", "rohan"])
    print("capitalised :", names.apply(str.capitalize).tolist())
    print("name lengths:", names.apply(len).tolist())
    print("grade distribution:\n", marks.apply(grade).value_counts())
    print("\nTip: prefer vectorised ops (marks * 0.1) when they exist – apply() is a loop.")


if __name__ == "__main__":
    value_counts_demo()
    apply_demo()
