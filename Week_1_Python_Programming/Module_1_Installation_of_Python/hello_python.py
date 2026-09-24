#! /usr/bin/env python3
"""
hello_python.py
---------------
Module 1 - Overview of Python: Starting with Python.

Your very first Python program. It shows the absolute basics:
printing, comments, variables, simple arithmetic, and how a script
is organised with a `main()` function and the `if __name__ == "__main__":` guard.

Run:  python hello_python.py
"""

import sys


# ---------------------------------------------------------------
# 1. Printing text
# ---------------------------------------------------------------
def say_hello() -> None:
    """Print the classic first message."""
    print("Hello, Python!")
    print("Welcome to the MysticML Journey - Week 1 🚀")


# ---------------------------------------------------------------
# 2. Variables and simple arithmetic (Python is dynamically typed)
# ---------------------------------------------------------------
def quick_tour() -> None:
    """Show variables, arithmetic operators and the type() function."""
    a = 7          # int
    b = 2          # int
    pi = 3.14159   # float
    language = "Python"  # str

    print("\n--- Arithmetic ---")
    print(f"{a} + {b}  = {a + b}")
    print(f"{a} - {b}  = {a - b}")
    print(f"{a} * {b}  = {a * b}")
    print(f"{a} / {b}  = {a / b}    (true division -> float)")
    print(f"{a} // {b} = {a // b}      (floor division)")
    print(f"{a} % {b}  = {a % b}      (remainder / modulo)")
    print(f"{a} ** {b} = {a ** b}     (power)")

    print("\n--- Types ---")
    for value in (a, pi, language, True, None):
        print(f"{value!r:>10} -> {type(value).__name__}")


# ---------------------------------------------------------------
# 3. Python is interpreted: every line is executed top to bottom
# ---------------------------------------------------------------
def about_interpreter() -> None:
    """Print which interpreter is running this file."""
    print("\n--- Interpreter ---")
    print(f"Python version : {sys.version.split()[0]}")
    print(f"Executable     : {sys.executable}")


def main() -> None:
    """Entry point."""
    say_hello()
    quick_tour()
    about_interpreter()
    # The Zen of Python - try `import this` in a Python shell!
    print("\nTip: type `import this` in a Python shell to read the Zen of Python.")


if __name__ == "__main__":
    main()
