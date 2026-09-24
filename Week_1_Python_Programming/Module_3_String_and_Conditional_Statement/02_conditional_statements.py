#! /usr/bin/env python3
"""
02_conditional_statements.py
----------------------------
Module 3 - If / Else statements and the single-line (ternary) if-else.

Covers:
  * if, if-else, if-elif-else ladders
  * nested if, logical operators (and / or / not), chained comparisons
  * single-hand (one-line) if-else  ->  value_if_true if cond else value_if_false
  * truthy / falsy values in conditions
  * match-case (Python 3.10+) as a modern alternative to long elif chains
  * an interactive grade calculator (use --demo for a non-interactive run)

Run:  python 02_conditional_statements.py          (asks for a score)
      python 02_conditional_statements.py --demo   (no input needed)
"""
import sys


# ---------------------------------------------------------------
# 1. if / if-else / if-elif-else
# ---------------------------------------------------------------
def basic_if_demo(temperature: int) -> None:
    """Show the three basic shapes of an if statement."""
    print(f"=== 1. Basic if (temperature = {temperature}) ===")
    if temperature > 35:                       # plain if
        print("It's very hot - stay hydrated!")

    if temperature >= 20:                      # if-else
        print("Wear a T-shirt.")
    else:
        print("Take a jacket.")

    if temperature < 0:                        # if-elif-else ladder
        print("Freezing")
    elif temperature < 15:
        print("Cold")
    elif temperature < 30:
        print("Pleasant")
    else:
        print("Hot")
    print()


# ---------------------------------------------------------------
# 2. Nested if, logical operators, chained comparisons
# ---------------------------------------------------------------
def logical_demo(age: int, has_ticket: bool) -> None:
    """Combine conditions with and / or / not and nesting."""
    print(f"=== 2. Nested & logical (age={age}, has_ticket={has_ticket}) ===")
    if has_ticket:
        if age >= 18:
            print("Entry allowed.")
        else:
            print("Entry allowed with a guardian.")
    else:
        print("Please buy a ticket first.")

    if age >= 18 and has_ticket:
        print("and : adult with ticket")
    if age < 12 or age > 60:
        print("or  : eligible for a discount")
    if not has_ticket:
        print("not : no ticket")
    if 13 <= age <= 19:                        # chained comparison
        print("chained: teenager")
    print()


# ---------------------------------------------------------------
# 3. Single-hand (one-line) if-else  a.k.a. ternary operator
# ---------------------------------------------------------------
def single_line_demo() -> None:
    """value_if_true if condition else value_if_false."""
    print("=== 3. Single-line if-else ===")
    for n in (-4, 0, 7):
        parity = "even" if n % 2 == 0 else "odd"
        sign = "positive" if n > 0 else "zero" if n == 0 else "negative"   # nested ternary
        print(f"{n:>3} is {parity:<4} and {sign}")
    x = 15
    if x > 10: print("one-line if (no else) also works, but use sparingly")  # noqa: E701
    maximum = a if (a := 8) > (b := 5) else b   # ternary + walrus
    print("max(8, 5) via ternary ->", maximum)
    print()


# ---------------------------------------------------------------
# 4. Truthy / falsy values
# ---------------------------------------------------------------
def truthiness_demo() -> None:
    """Empty containers, 0, None and '' are False in a condition."""
    print("=== 4. Truthy / falsy ===")
    for value in [0, 1, "", "text", [], [0], None, {}, {"k": 1}]:
        print(f"{value!r:10} -> {'truthy' if value else 'falsy'}")
    print()


# ---------------------------------------------------------------
# 5. match-case (structural pattern matching, Python 3.10+)
# ---------------------------------------------------------------
def http_status(code: int) -> str:
    """Translate an HTTP status code with match-case."""
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500 | 502 | 503:
            return "Server Error"
        case _:
            return "Unknown"


# ---------------------------------------------------------------
# 6. Mini project: grade calculator
# ---------------------------------------------------------------
def grade(score: float) -> str:
    """Return a letter grade for a 0-100 score."""
    if not 0 <= score <= 100:
        return "Invalid score"
    elif score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"


def main() -> None:
    """Run demos; ask for a score unless --demo is given."""
    basic_if_demo(28)
    logical_demo(age=16, has_ticket=True)
    single_line_demo()
    truthiness_demo()
    print("=== 5. match-case ===")
    for code in (200, 404, 503, 418):
        print(code, "->", http_status(code))
    print()

    print("=== 6. Grade calculator ===")
    if "--demo" in sys.argv or not sys.stdin.isatty():
        for s in (95, 81, 64, 45, 12, 120):
            print(f"score {s:>3} -> {grade(s)}")
    else:
        raw = input("Enter your score (0-100): ")
        try:
            print("Your grade:", grade(float(raw)))
        except ValueError:
            print("That was not a number!")


if __name__ == "__main__":
    main()
