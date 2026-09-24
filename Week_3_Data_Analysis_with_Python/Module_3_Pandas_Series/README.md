# Module 3 – Pandas (Series)
> Week 3 · Data Analysis with Python   |   ⬅ Previous: [Module 2 – Introduction to Pandas](../Module_2_Introduction_to_Pandas)  ·  Next ➡: [Module 4 – Pandas DataFrame](../Module_4_Pandas_DataFrame)

## 🎯 Learning Objectives
- Understand the parts of a Series (values, index, name, dtype) and create one from any source
- Explain how a Series differs from a Python list, and use vectorised operations
- Use common Series functions, sort values and indexes, and extract values by label or position
- Summarise categories with `.value_counts()` and transform values with `.apply()`
- Clean data by handling duplicates and missing values

## ✅ Syllabus Checklist
- [x] Concept Of Series in Pandas | Creating Series using Pandas
- [x] Series vs List, Series Operations
- [x] Different Functions in Series | Sorting of Series
- [x] Extracting Values from Series
- [x] `.value_counts()` method, `.apply()` methods
- [x] Data Cleaning – Dealing with Duplicates and Missing Values

## 📖 Concepts

### What is a Series?
```
index   values
Aadil     88      <- name="marks", dtype=int64
Yaana     72
Sama      95
```
A Series is a **NumPy array with labels**. Create it from a list, NumPy array, dict (keys become the index) or scalar.

### Series vs list
| | Python list | pandas Series |
|---|---|---|
| Labels | positions only | any labels |
| `x * 2` | repeats the list | multiplies each value |
| Types | any mix | one dtype |
| Missing data | `None` breaks maths | `NaN` is skipped by stats |
| Speed | Python loop | vectorised C code |

**Index alignment:** `s1 + s2` matches values **by label**, and gives `NaN` where a label exists on one side only. Use `s1.add(s2, fill_value=0)` to avoid that.

### Extracting values
| Syntax | Based on | Slice end |
|---|---|---|
| `s.loc["a"]`, `s.at["a"]` | label | included |
| `s.iloc[0]`, `s.iat[0]` | position | excluded |
| `s[s > 80]` | boolean mask | – |

### Sorting
`sort_values(ascending=False, na_position="first", kind="mergesort")` and `sort_index()`. `kind` picks the algorithm: `quicksort` (default), `mergesort`/`stable` (keep ties in their original order), `heapsort`.

### value_counts & apply
```python
s.value_counts()                 # frequency table
s.value_counts(normalize=True)   # proportions
s.value_counts(dropna=False)     # include NaN
s.apply(func)                    # run func on every element
```

### Cleaning
| Problem | Detect | Fix |
|---|---|---|
| Duplicates | `duplicated(keep=...)` | `drop_duplicates()` |
| Missing | `isna()`, `hasnans` | `dropna()`, `fillna(value / mean / median / mode)`, `ffill`, `bfill`, `interpolate` |

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `01_creating_series.py` | Series anatomy, creating from list/array/dict/scalar/date range |
| `02_series_vs_list_and_operations.py` | List vs Series comparison & timing, arithmetic, index alignment, comparisons, `.str`/`.dt` accessors |
| `03_series_functions_sorting.py` | head/describe/stats/idxmax/cumsum/unique/map/clip, `sort_values`, `sort_index`, `kind=` algorithms, `rank` |
| `04_extracting_values.py` | `[]`, `loc`, `iloc`, `at`, `iat`, `get`, slicing, masks, `where`/`mask`, nlargest, conversions |
| `05_value_counts_apply.py` | All `value_counts` options (normalize, dropna, bins) and `apply` with functions, lambdas and extra args |
| `06_data_cleaning.py` | Duplicates (`keep=`), missing values: detect, drop, fill, ffill/bfill, interpolate, text placeholders |

## ▶️ How to Run
```bash
cd Week_3_Data_Analysis_with_Python/Module_3_Pandas_Series
python 01_creating_series.py
python 02_series_vs_list_and_operations.py
python 03_series_functions_sorting.py
python 04_extracting_values.py
python 05_value_counts_apply.py
python 06_data_cleaning.py
```

## 🧠 Key Takeaways
- Operations between Series align on the **index**, not on position.
- `loc` works with labels and includes the slice end; `iloc` works with positions and excludes it.
- `value_counts()` is the quickest way to understand a categorical column.
- Prefer vectorised operations. Reach for `apply()` only when no built-in method exists.
- Decide how to handle missing data deliberately: drop it, fill it, or interpolate it.

## 📝 Practice Exercises
1. Create a Series of 7 daily temperatures indexed by weekday names; print the hottest day and the days above the mean.
2. Given `pd.Series(["red", "blue", "red", None, "green", "red"])`, show the percentage of each colour, including missing values.
3. Use `apply()` to convert a Series of temperatures in °C into °F, labelled "cold" or "warm".
4. Clean `pd.Series([5, None, 7, 7, None, 10, 5])`: remove duplicates, then fill the gaps with interpolation.
