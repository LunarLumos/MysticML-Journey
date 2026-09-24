#! /usr/bin/env python3
"""
01_primitive_and_core_types.py
------------------------------
Module 2 - Primitive and Core Data Types.

Covers:
  * variables and dynamic typing
  * primitive (scalar) types: int, float, complex, bool, str, NoneType, bytes
  * core container types: list, tuple, dict, set, frozenset, range
  * type checking with type() / isinstance()
  * type conversion (casting) and truthiness

Run:  python 01_primitive_and_core_types.py
"""


# ---------------------------------------------------------------
# 1. Variables - a name that points to an object
# ---------------------------------------------------------------
def variables_demo() -> None:
    """Show assignment, multiple assignment, swapping and naming rules."""
    print("=== 1. Variables ===")
    age = 25                      # snake_case is the Python convention
    x, y, z = 1, 2, 3             # multiple assignment
    a = b = c = 0                 # same value to several names
    x, y = y, x                   # swap without a temp variable
    print(f"age={age}, x={x}, y={y}, z={z}, a={a}, b={b}, c={c}")

    value = 10                    # dynamic typing: the NAME has no type,
    print(f"value={value!r:<8} type={type(value).__name__}")
    value = "ten"                 # ...the OBJECT it points to does
    print(f"value={value!r:<8} type={type(value).__name__}")
    MAX_SPEED = 120               # UPPER_CASE = constant by convention
    print(f"MAX_SPEED={MAX_SPEED}\n")


# ---------------------------------------------------------------
# 2. Primitive data types
# ---------------------------------------------------------------
def primitive_types_demo() -> None:
    """Print one example of every primitive type plus a few facts about it."""
    print("=== 2. Primitive data types ===")
    samples = [
        42,                # int     - unlimited precision
        2 ** 100,          # int     - still exact!
        3.14,              # float   - 64-bit IEEE-754
        1.5e-3,            # float   - scientific notation
        2 + 3j,            # complex - real + imaginary
        True,              # bool    - subclass of int (True == 1)
        "hello",           # str     - Unicode text
        b"bytes",          # bytes   - raw 8-bit data
        None,              # NoneType - "no value"
    ]
    for value in samples:
        print(f"{value!r:<35} -> {type(value).__name__}")

    print("\nFun facts:")
    print(f"0.1 + 0.2 = {0.1 + 0.2}  (floats are approximate!)")
    print(f"round(0.1 + 0.2, 2) = {round(0.1 + 0.2, 2)}")
    print(f"True + True = {True + True}   (bool is a subclass of int)")
    print(f"(2+3j).real = {(2 + 3j).real}, .imag = {(2 + 3j).imag}")
    print(f"int max? Python ints never overflow: 2**100 = {2 ** 100}\n")


# ---------------------------------------------------------------
# 3. Core (built-in) container types
# ---------------------------------------------------------------
def core_types_demo() -> None:
    """Show the built-in collections and their key properties."""
    print("=== 3. Core container types ===")
    rows = [
        ("list", [1, 2, 2, 3], "ordered, mutable, allows duplicates"),
        ("tuple", (1, 2, 2, 3), "ordered, IMMUTABLE, allows duplicates"),
        ("dict", {"a": 1, "b": 2}, "key -> value, insertion-ordered, mutable"),
        ("set", {1, 2, 2, 3}, "unordered, mutable, unique items only"),
        ("frozenset", frozenset({1, 2}), "immutable set (hashable)"),
        ("range", range(0, 10, 2), "lazy immutable sequence of ints"),
    ]
    for name, obj, note in rows:
        print(f"{name:<10} {obj!r:<25} {note}")
    print()


# ---------------------------------------------------------------
# 4. Checking types
# ---------------------------------------------------------------
def type_checking_demo() -> None:
    """type() vs isinstance()."""
    print("=== 4. type() vs isinstance() ===")
    n = True
    print(f"type(True) is int      -> {type(n) is int}")
    print(f"isinstance(True, int)  -> {isinstance(n, int)}  (respects inheritance)")
    print(f"isinstance(3.0, (int, float)) -> {isinstance(3.0, (int, float))}\n")


# ---------------------------------------------------------------
# 5. Type conversion (casting)
# ---------------------------------------------------------------
def conversion_demo() -> None:
    """Explicit and implicit type conversion."""
    print("=== 5. Type conversion ===")
    print(f"int('42')       = {int('42')}")
    print(f"int(3.99)       = {int(3.99)}   (truncates toward zero)")
    print(f"float('2.5')    = {float('2.5')}")
    print(f"str(100) + '!'  = {str(100) + '!'}")
    print(f"int('ff', 16)   = {int('ff', 16)}   (base conversion)")
    print(f"bool('')        = {bool('')},  bool('0') = {bool('0')}")
    print(f"list('abc')     = {list('abc')}")
    print(f"tuple([1, 2])   = {tuple([1, 2])}")
    print(f"set([1, 1, 2])  = {set([1, 1, 2])}")
    print(f"dict([('a', 1)]) = {dict([('a', 1)])}")
    print(f"implicit: 3 + 4.5 = {3 + 4.5} (int promoted to float)")
    try:
        int("hello")
    except ValueError as err:
        print(f"int('hello') -> ValueError: {err}")
    print()


# ---------------------------------------------------------------
# 6. Truthiness - every object is True or False in an `if`
# ---------------------------------------------------------------
def truthiness_demo() -> None:
    """Show which values are 'falsy'."""
    print("=== 6. Truthiness ===")
    for value in [0, 0.0, "", [], (), {}, set(), None, 1, "a", [0]]:
        print(f"{value!r:<8} -> {bool(value)}")


def main() -> None:
    """Run every demo in order."""
    variables_demo()
    primitive_types_demo()
    core_types_demo()
    type_checking_demo()
    conversion_demo()
    truthiness_demo()


if __name__ == "__main__":
    main()
