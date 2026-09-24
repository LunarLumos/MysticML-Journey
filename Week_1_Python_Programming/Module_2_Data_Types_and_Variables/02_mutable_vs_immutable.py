#! /usr/bin/env python3
"""
02_mutable_vs_immutable.py
--------------------------
Module 2 - Mutable and Immutable Data Types.

We use id() (the object's identity - its memory address in CPython) to SEE
whether an operation changes an object in place (mutable) or creates a brand
new object (immutable).

  Immutable: int, float, complex, bool, str, bytes, tuple, frozenset, None
  Mutable  : list, dict, set, bytearray, (most user-defined objects)

Run:  python 02_mutable_vs_immutable.py
"""


def show(label: str, obj: object) -> int:
    """Print an object with its id and return the id."""
    print(f"{label:<28} value={obj!r:<22} id={id(obj)}")
    return id(obj)


# ---------------------------------------------------------------
# 1. Immutable objects: "changing" them creates a NEW object
# ---------------------------------------------------------------
def immutable_demo() -> None:
    """int, str and tuple get a new id when 'modified'."""
    print("=== 1. Immutable types ===")
    n = 10
    before = show("n = 10", n)
    n += 1
    after = show("n += 1", n)
    print(f"  same object? {before == after}  -> a new int was created\n")

    s = "hello"
    before = show("s = 'hello'", s)
    s += " world"
    after = show("s += ' world'", s)
    print(f"  same object? {before == after}  -> strings are immutable")
    try:
        s[0] = "H"  # type: ignore[index]
    except TypeError as err:
        print(f"  s[0] = 'H' -> TypeError: {err}\n")

    t = (1, 2, 3)
    before = show("t = (1, 2, 3)", t)
    t += (4,)
    after = show("t += (4,)", t)
    print(f"  same object? {before == after}  -> tuples are immutable")
    try:
        t[0] = 99  # type: ignore[index]
    except TypeError as err:
        print(f"  t[0] = 99 -> TypeError: {err}\n")


# ---------------------------------------------------------------
# 2. Mutable objects: changed IN PLACE, id stays the same
# ---------------------------------------------------------------
def mutable_demo() -> None:
    """list, dict and set keep their id when modified."""
    print("=== 2. Mutable types ===")
    nums = [1, 2, 3]
    before = show("nums = [1, 2, 3]", nums)
    nums.append(4)
    after = show("nums.append(4)", nums)
    print(f"  same object? {before == after}  -> modified in place\n")

    d = {"a": 1}
    before = show("d = {'a': 1}", d)
    d["b"] = 2
    after = show("d['b'] = 2", d)
    print(f"  same object? {before == after}\n")

    st = {1, 2}
    before = show("st = {1, 2}", st)
    st.add(3)
    after = show("st.add(3)", st)
    print(f"  same object? {before == after}\n")


# ---------------------------------------------------------------
# 3. Aliasing: two names, ONE object
# ---------------------------------------------------------------
def aliasing_demo() -> None:
    """Why mutability matters: changes are visible through every alias."""
    print("=== 3. Aliasing ===")
    a = [1, 2, 3]
    b = a                  # b is NOT a copy - same object
    b.append(99)
    print(f"a = {a}, b = {b}, a is b -> {a is b}")

    c = a.copy()           # shallow copy -> new list
    c.append(100)
    print(f"a = {a}, c = {c}, a is c -> {a is c}")

    x = 5
    y = x
    y += 1                 # rebinding y does not affect x (int is immutable)
    print(f"x = {x}, y = {y}\n")


# ---------------------------------------------------------------
# 4. Shallow vs deep copy
# ---------------------------------------------------------------
def copy_demo() -> None:
    """Nested mutable objects need deepcopy."""
    import copy

    print("=== 4. Shallow vs deep copy ===")
    original = [[1, 2], [3, 4]]
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)
    original[0].append("X")
    print(f"original = {original}")
    print(f"shallow  = {shallow}   <- inner list is shared!")
    print(f"deep     = {deep}   <- fully independent\n")


# ---------------------------------------------------------------
# 5. Gotcha: tuple containing a list, and mutable default args
# ---------------------------------------------------------------
def gotchas_demo() -> None:
    """Two classic traps."""
    print("=== 5. Gotchas ===")
    t = ([1, 2], 3)
    t[0].append(3)  # the tuple is immutable, but the list inside is not
    print(f"tuple with a list inside after t[0].append(3): {t}")

    def add_item_bad(item, bucket=[]):  # noqa: B006 - intentional demo
        bucket.append(item)
        return bucket

    def add_item_good(item, bucket=None):
        if bucket is None:
            bucket = []
        bucket.append(item)
        return bucket

    print(f"bad : {add_item_bad(1)} then {add_item_bad(2)}  <- default list is shared!")
    print(f"good: {add_item_good(1)} then {add_item_good(2)}")

    print("\nHashability: only immutable objects can be dict keys / set items")
    print(f"  {{(1, 2): 'ok'}} -> {({(1, 2): 'ok'})}")
    try:
        {[1, 2]: "fail"}  # noqa: B018
    except TypeError as err:
        print(f"  {{[1, 2]: ...}} -> TypeError: {err}")


def main() -> None:
    """Run all demos."""
    immutable_demo()
    mutable_demo()
    aliasing_demo()
    copy_demo()
    gotchas_demo()


if __name__ == "__main__":
    main()
