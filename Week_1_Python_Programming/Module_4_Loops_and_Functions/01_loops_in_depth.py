#! /usr/bin/env python3
"""
01_loops_in_depth.py
--------------------
Module 4 - What are loops? While loop and for loop.

Covers:
  * while loops (counter, sentinel, while-else, infinite loop + break)
  * for loops over range, strings, lists, dicts, enumerate and zip
  * break, continue, pass and the loop-else clause
  * nested loops (multiplication table, pattern printing)

Run:  python 01_loops_in_depth.py
"""


# ---------------------------------------------------------------
# 1. While loop - repeat WHILE a condition is True
# ---------------------------------------------------------------
def while_loop_demo() -> None:
    """Counter loop, sentinel loop, break and while-else."""
    print("=== 1. While loop ===")
    count = 1
    while count <= 5:                 # counter-controlled
        print("count =", count)
        count += 1                    # forgetting this => infinite loop!

    # Sentinel-controlled: keep halving until the value is small
    value = 100
    steps = 0
    while value > 1:
        value /= 2
        steps += 1
    print(f"100 halved {steps} times -> {value:.3f}")

    # while True + break (common for menus / retry logic)
    attempts = ["1234", "abcd", "secret"]
    i = 0
    while True:
        guess = attempts[i]
        i += 1
        if guess == "secret":
            print(f"Password found after {i} attempts")
            break

    # while-else: else runs only if the loop was NOT broken
    n = 3
    while n > 0:
        n -= 1
    else:
        print("while-else: loop finished normally")
    print()


# ---------------------------------------------------------------
# 2. For loop - iterate over ANY iterable
# ---------------------------------------------------------------
def for_loop_demo() -> None:
    """range(), strings, lists, dicts, enumerate, zip, reversed."""
    print("=== 2. For loop ===")
    print("range(5)        :", [i for i in range(5)])
    print("range(2, 10, 3) :", list(range(2, 10, 3)))
    print("range(5, 0, -1) :", list(range(5, 0, -1)))

    for ch in "ML!":
        print("char:", ch)

    fruits = ["apple", "banana", "cherry"]
    for idx, fruit in enumerate(fruits, start=1):
        print(f"{idx}. {fruit}")

    prices = [1.2, 0.5, 3.0]
    for fruit, price in zip(fruits, prices):
        print(f"{fruit:<7} costs {price}")

    stock = {"pens": 10, "books": 3}
    for item, qty in stock.items():
        print(f"{item} -> {qty}")

    total = 0
    for x in range(1, 101):
        total += x
    print("sum 1..100 =", total)
    print("reversed    :", [f for f in reversed(fruits)])
    print()


# ---------------------------------------------------------------
# 3. Loop control: break, continue, pass, for-else
# ---------------------------------------------------------------
def loop_control_demo() -> None:
    """Change the normal flow of a loop."""
    print("=== 3. break / continue / pass / for-else ===")
    for n in range(1, 10):
        if n == 6:
            break                     # leave the loop completely
        if n % 2 == 0:
            continue                  # skip to the next iteration
        print("odd before 6:", n)

    for n in range(3):
        pass                          # placeholder - do nothing (yet)

    # for-else: classic prime check
    for number in (7, 9):
        for d in range(2, number):
            if number % d == 0:
                print(f"{number} is not prime (divisible by {d})")
                break
        else:
            print(f"{number} is prime")
    print()


# ---------------------------------------------------------------
# 4. Nested loops
# ---------------------------------------------------------------
def nested_loops_demo() -> None:
    """Multiplication table and a star pyramid."""
    print("=== 4. Nested loops ===")
    for i in range(1, 4):
        row = ""
        for j in range(1, 6):
            row += f"{i * j:4}"
        print(row)
    height = 4
    for level in range(1, height + 1):
        print(" " * (height - level) + "*" * (2 * level - 1))
    print()


def main() -> None:
    """Run every demo."""
    while_loop_demo()
    for_loop_demo()
    loop_control_demo()
    nested_loops_demo()


if __name__ == "__main__":
    main()
