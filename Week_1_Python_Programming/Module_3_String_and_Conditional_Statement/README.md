# Module 3 – String and Conditional Statement in Python
> Week 1 · Python Programming   |   ⬅ Previous: [Module 2 – Data Types and Variables](../Module_2_Data_Types_and_Variables)  ·  Next ➡: [Module 4 – Loops and Functions](../Module_4_Loops_and_Functions)

## 🎯 Learning Objectives
- Create, index and slice strings and understand that they are **immutable**.
- Use the most important **string methods** for cleaning and searching text.
- Format output with **`str.format()`** (and f-strings).
- Make decisions with **if / elif / else**, logical operators and the **single-line if-else**.

## ✅ Syllabus Checklist
- [x] String
- [x] String built-in methods
- [x] String formatting using format function
- [x] If – Else Statement | Single Hand if else

## 📖 Concepts

### 1. Strings
A string is an immutable sequence of Unicode characters: `'..'`, `".."`, `"""multi-line"""`, `r"raw\path"`.
```python
s = "Python"
s[0]      # 'P'        s[-1]   # 'n'
s[1:4]    # 'yth'      s[::-1] # 'nohtyP'
s[0] = "J"  # ❌ TypeError – build a new string instead: "J" + s[1:]
```
Slicing syntax: `s[start:stop:step]` — `stop` is **excluded**.

### 2. String methods (they always return a *new* string/value)
| Purpose | Methods |
|---|---|
| Case | `upper() lower() title() capitalize() swapcase() casefold()` |
| Whitespace | `strip() lstrip() rstrip()` |
| Search | `find() rfind() index() count() startswith() endswith()` |
| Split / join | `split() rsplit() splitlines() partition() "sep".join(list)` |
| Replace | `replace(old, new, count)` |
| Checks | `isalpha() isdigit() isalnum() isspace() isupper() islower() istitle()` |
| Padding | `center() ljust() rjust() zfill()` |

### 3. Formatting with `format()`
```python
"{} is {} years".format("Alice", 30)        # positional
"{1} before {0}".format("a", "b")           # by index
"{name} scored {s:.2f}".format(name="Bo", s=9.456)  # keyword + 2 decimals
"{:<10}|{:^10}|{:>10}".format("L", "C", "R")        # alignment
"{:,}  {:.1%}  {:05d}".format(1234567, 0.876, 42)   # 1,234,567  87.6%  00042
```
Format spec: `{[field]:[fill][align][width][,][.precision][type]}`. f-strings (`f"{x:.2f}"`) use the same mini-language.

### 4. Conditional statements
```python
if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
else:
    grade = "C"
```
- Logical operators: `and`, `or`, `not`; chained comparisons: `13 <= age <= 19`.
- **Falsy** values: `0, 0.0, "", [], {}, set(), None, False` — everything else is truthy.
- **Single-hand (ternary) if-else**: `result = "even" if n % 2 == 0 else "odd"`
- Python 3.10+: `match value: case 200: ... case _: ...`

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `string_and_conditional_statement.py` | *(original learner script)* strip/upper/lower/replace/split, `format()`, if-elif-else, ternary, slicing, a greeting based on `input()` |
| `01_string_methods_and_formatting.py` | string creation, slicing, immutability, ~35 string methods, full `str.format()` tour, f-strings, `%` style |
| `02_conditional_statements.py` | if / if-else / elif ladders, nested ifs, logical ops, single-line if-else, truthiness, `match-case`, grade calculator |

## ▶️ How to Run
```bash
cd Week_1_Python_Programming/Module_3_String_and_Conditional_Statement
python string_and_conditional_statement.py     # asks for your name
python 01_string_methods_and_formatting.py
python 02_conditional_statements.py            # asks for a score
python 02_conditional_statements.py --demo     # non-interactive
```

## 🧠 Key Takeaways
- Strings never change in place; methods return new strings.
- `find()` returns `-1` when not found, `index()` raises `ValueError`.
- `format()` / f-strings give full control over width, alignment and precision.
- Keep `elif` ladders ordered from most to least specific; use the ternary only for short, simple choices.

## 📝 Practice Exercises
1. Check whether a word is a palindrome (ignore case and spaces).
2. Count vowels in a sentence using a loop and `in "aeiou"`.
3. Print a receipt table (item, qty, price, total) aligned with `format()`.
4. Write a BMI calculator that prints *Underweight / Normal / Overweight / Obese*.
5. Using a single-line if-else, label a year as "Leap" or "Not leap".
