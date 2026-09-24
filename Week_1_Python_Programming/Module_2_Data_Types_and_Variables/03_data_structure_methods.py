#! /usr/bin/env python3
"""
03_data_structure_methods.py
----------------------------
Module 2 - Working with lists, tuples, dictionaries and sets.

A guided tour of (almost) every built-in method of the four core
data structures, plus the most useful built-in functions that work
on them (len, sorted, min, max, sum, zip, enumerate, any, all).

Run:  python 03_data_structure_methods.py
"""


# ---------------------------------------------------------------
# 1. Lists - ordered, mutable, allow duplicates
# ---------------------------------------------------------------
def list_methods() -> None:
    """Demonstrate every list method."""
    print("=== 1. LIST methods ===")
    nums = [5, 3, 8]
    nums.append(1)                  # add one item at the end
    print("append(1)        ->", nums)
    nums.extend([9, 3])             # add many items
    print("extend([9, 3])   ->", nums)
    nums.insert(0, 42)              # insert at index 0
    print("insert(0, 42)    ->", nums)
    nums.remove(3)                  # remove FIRST occurrence of value 3
    print("remove(3)        ->", nums)
    last = nums.pop()               # remove + return last item
    print(f"pop()            -> {nums} (popped {last})")
    first = nums.pop(0)             # remove + return item at index
    print(f"pop(0)           -> {nums} (popped {first})")
    print("index(8)         ->", nums.index(8))
    print("count(3)         ->", nums.count(3))
    nums.sort()                     # in-place ascending sort
    print("sort()           ->", nums)
    nums.sort(reverse=True)
    print("sort(reverse)    ->", nums)
    nums.reverse()                  # in-place reverse
    print("reverse()        ->", nums)
    backup = nums.copy()            # shallow copy
    nums.clear()                    # empty the list
    print(f"clear()          -> {nums}  (copy kept: {backup})")

    # Indexing & slicing
    letters = list("python")
    print("letters[0], letters[-1] ->", letters[0], letters[-1])
    print("letters[1:4]            ->", letters[1:4])
    print("letters[::-1]           ->", letters[::-1])
    print()


# ---------------------------------------------------------------
# 2. Tuples - ordered, IMMUTABLE, allow duplicates
# ---------------------------------------------------------------
def tuple_methods() -> None:
    """Tuples only have two methods: count() and index()."""
    print("=== 2. TUPLE methods ===")
    point = (3, 4, 3, 7)
    print("count(3)  ->", point.count(3))
    print("index(7)  ->", point.index(7))
    single = (5,)                   # a one-item tuple needs a comma!
    print("type((5,)) ->", type(single), "| type((5)) ->", type((5)))
    x, y, *rest = point             # tuple unpacking
    print(f"unpacking  -> x={x}, y={y}, rest={rest}")
    print("concat     ->", point + (10,))
    print("repeat     ->", ("ab",) * 3)
    print()


# ---------------------------------------------------------------
# 3. Dictionaries - key -> value mapping (insertion ordered)
# ---------------------------------------------------------------
def dict_methods() -> None:
    """Demonstrate every dict method."""
    print("=== 3. DICT methods ===")
    student = {"name": "Asha", "age": 21}
    print("get('name')            ->", student.get("name"))
    print("get('city', 'N/A')     ->", student.get("city", "N/A"))
    student.update({"age": 22, "city": "Pune"})
    print("update(...)            ->", student)
    print("keys()                 ->", list(student.keys()))
    print("values()               ->", list(student.values()))
    print("items()                ->", list(student.items()))
    print("setdefault('grade','A')->", student.setdefault("grade", "A"), student)
    city = student.pop("city")
    print(f"pop('city')            -> {student} (removed {city})")
    last_item = student.popitem()   # removes the LAST inserted pair
    print(f"popitem()              -> {student} (removed {last_item})")
    print("fromkeys(['a','b'], 0) ->", dict.fromkeys(["a", "b"], 0))
    clone = student.copy()
    student.clear()
    print(f"clear()                -> {student} (copy kept: {clone})")

    # Looping over a dictionary
    marks = {"math": 90, "physics": 78, "chem": 85}
    for subject, score in marks.items():
        print(f"   {subject:<8} {score}")
    print("merge with |           ->", marks | {"bio": 88})
    print()


# ---------------------------------------------------------------
# 4. Sets - unordered, mutable, UNIQUE items
# ---------------------------------------------------------------
def set_methods() -> None:
    """Demonstrate set methods and set algebra."""
    print("=== 4. SET methods ===")
    a = {1, 2, 3, 4}
    b = {3, 4, 5}
    a.add(10)
    print("add(10)                 ->", a)
    a.update([11, 12])
    print("update([11, 12])        ->", a)
    a.remove(12)                    # KeyError if missing
    a.discard(999)                  # silently ignores missing items
    print("remove(12)/discard(999) ->", a)
    print("pop() (arbitrary item)  ->", a.pop(), a)
    print("union        a | b      ->", a | b, "=", a.union(b))
    print("intersection a & b      ->", a & b, "=", a.intersection(b))
    print("difference   a - b      ->", a - b, "=", a.difference(b))
    print("symmetric    a ^ b      ->", a ^ b, "=", a.symmetric_difference(b))
    print("{3,4}.issubset(b)       ->", {3, 4}.issubset(b))
    print("b.issuperset({5})       ->", b.issuperset({5}))
    print("a.isdisjoint({100})     ->", a.isdisjoint({100}))
    c = a.copy()
    c.intersection_update(b)
    print("intersection_update     ->", c)
    c.clear()
    print("clear()                 ->", c)
    print("dedupe a list           ->", sorted(set([3, 1, 3, 2, 1])))
    print()


# ---------------------------------------------------------------
# 5. Built-in functions that work on every collection
# ---------------------------------------------------------------
def builtin_functions() -> None:
    """len, min, max, sum, sorted, zip, enumerate, any, all, in."""
    print("=== 5. Handy built-ins ===")
    scores = [72, 95, 88, 60]
    names = ["Ravi", "Meera", "John", "Zara"]
    print("len / min / max / sum ->", len(scores), min(scores), max(scores), sum(scores))
    print("sorted(desc)          ->", sorted(scores, reverse=True))
    print("zip -> dict           ->", dict(zip(names, scores)))
    for i, name in enumerate(names, start=1):
        print(f"   {i}. {name}")
    print("any(>90) / all(>50)   ->", any(s > 90 for s in scores), all(s > 50 for s in scores))
    print("'John' in names       ->", "John" in names)
    print()


def main() -> None:
    """Run every demo in order."""
    list_methods()
    tuple_methods()
    dict_methods()
    set_methods()
    builtin_functions()


if __name__ == "__main__":
    main()
