# Module 2 – Data Types and Variables
> Week 1 · Python Programming   |   ⬅ Previous: [Module 1 – Installation of Python](../Module_1_Installation_of_Python)  ·  Next ➡: [Module 3 – String and Conditional Statement](../Module_3_String_and_Conditional_Statement)

## 🎯 Learning Objectives
- Create variables and understand Python's **dynamic typing**.
- Know every **primitive** type (`int`, `float`, `complex`, `bool`, `str`, `None`, `bytes`) and **core** container type.
- Explain **mutable vs immutable** objects using `id()` and avoid aliasing bugs.
- Use the methods of **lists, tuples, dictionaries and sets** fluently.

## ✅ Syllabus Checklist
- [x] Primitive and Core Datatype
- [x] Mutable and Immutable Data Types
- [x] Core built-in data structures – Lists, Tuples, Dictionaries, Sets
- [x] Working with list, tuple, dictionaries and sets and explore different functions and methods

## 📖 Concepts

### 1. Variables are names, not boxes
A variable is a **name bound to an object**. The object has the type, not the name:
```python
x = 10        # x -> int object 10
x = "ten"     # x now points to a str object (dynamic typing)
a, b = 1, 2   # multiple assignment
a, b = b, a   # swap without a temp variable
```
Naming rules: letters/digits/underscore, cannot start with a digit, case-sensitive, not a keyword. Convention: `snake_case`.

### 2. Primitive (scalar) vs core (container) types
| Category | Type | Example | Mutable? |
|---|---|---|---|
| Numeric | `int` | `42` | ❌ |
| Numeric | `float` | `3.14` | ❌ |
| Numeric | `complex` | `2+3j` | ❌ |
| Boolean | `bool` | `True` | ❌ |
| Text | `str` | `"hi"` | ❌ |
| Null | `NoneType` | `None` | ❌ |
| Sequence | `list` | `[1, 2]` | ✅ |
| Sequence | `tuple` | `(1, 2)` | ❌ |
| Sequence | `range` | `range(5)` | ❌ |
| Mapping | `dict` | `{"a": 1}` | ✅ |
| Set | `set` / `frozenset` | `{1, 2}` | ✅ / ❌ |

Check types with `type(x)` or (better) `isinstance(x, int)`. Convert with `int()`, `float()`, `str()`, `list()`, `tuple()`, `set()`, `bool()`.

### 3. Mutable vs immutable
- **Immutable** objects can't change in place — "modifying" them creates a *new* object, so `id()` changes.
- **Mutable** objects change in place — `id()` stays the same, and every name pointing at them sees the change.
```python
s = "hi";  before = id(s); s += "!";  id(s) == before   # False – new object
l = [1];   before = id(l); l.append(2); id(l) == before  # True  – same object
b = l      # alias! b.append(3) also changes l
c = l.copy()   # independent (shallow) copy; use copy.deepcopy for nested data
```
Classic gotcha: never use a mutable default argument (`def f(x=[])`) — use `None` instead.

### 4. The four core data structures
| | List | Tuple | Dict | Set |
|---|---|---|---|---|
| Literal | `[1, 2]` | `(1, 2)` | `{"k": 1}` | `{1, 2}` |
| Ordered | ✅ | ✅ | ✅ (insertion) | ❌ |
| Mutable | ✅ | ❌ | ✅ | ✅ |
| Duplicates | ✅ | ✅ | keys unique | ❌ |
| Key methods | `append extend insert remove pop index count sort reverse copy clear` | `count index` | `get keys values items update pop popitem setdefault fromkeys copy clear` | `add update remove discard pop union intersection difference symmetric_difference issubset issuperset isdisjoint` |

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `data_types_and_variables.py` | *(original learner script)* primitives, mutable/immutable examples, basic list/tuple/dict/set operations |
| `01_primitive_and_core_types.py` | variables, all primitive types, core containers, `type`/`isinstance`, casting, truthiness |
| `02_mutable_vs_immutable.py` | `id()` experiments, aliasing, shallow vs deep copy, mutable-default gotcha |
| `03_data_structure_methods.py` | every list/tuple/dict/set method + handy built-ins (`zip`, `enumerate`, `sorted`, `any`, `all`) |

## ▶️ How to Run
```bash
cd Week_1_Python_Programming/Module_2_Data_Types_and_Variables
python data_types_and_variables.py
python 01_primitive_and_core_types.py
python 02_mutable_vs_immutable.py
python 03_data_structure_methods.py
```

## 🧠 Key Takeaways
- Everything in Python is an object; variables are just labels.
- Immutable: numbers, `str`, `tuple`, `frozenset`. Mutable: `list`, `dict`, `set`.
- Assignment never copies — use `.copy()` / `copy.deepcopy()` when you need independence.
- Pick the structure by need: order + change → list; fixed record → tuple; lookup by key → dict; uniqueness/membership → set.

## 📝 Practice Exercises
1. Given `[4, 1, 4, 2, 1]`, produce the sorted unique values *and* a dict of value → count.
2. Prove with `id()` that `t = (1, 2); t += (3,)` creates a new tuple.
3. Create a nested list, copy it with `.copy()` and `copy.deepcopy()`, mutate an inner list and explain the difference.
4. Two friends' hobby sets: print hobbies they share, hobbies only one has, and all hobbies.
5. Invert a dictionary `{"a": 1, "b": 2}` → `{1: "a", 2: "b"}`.
