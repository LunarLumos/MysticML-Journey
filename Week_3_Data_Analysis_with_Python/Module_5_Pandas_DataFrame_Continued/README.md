# Module 5 – DataFrame (Continued)
> Week 3 · Data Analysis with Python   |   ⬅ Previous: [Module 4 – Pandas DataFrame](../Module_4_Pandas_DataFrame)  ·  Next ➡: [Module 6 – Data Visualization](../Module_6_Data_Visualization)

## 🎯 Learning Objectives
- Sort DataFrames by values or index, and choose the sorting algorithm (`kind=`)
- Filter rows with conditions, `isin`, `between`, string methods and `&` / `|` / `~`
- Manage the index with `set_index` and `reset_index`
- Read and write specific cells or rows with `loc`, `iloc`, `at` and `iat`
- Rename and delete labels, and use `nlargest`, `nsmallest`, `where`, `query` and `apply`

## ✅ Syllabus Checklist
- [x] Different Sorting Algorithms in DataFrame
- [x] Filtering Data in DataFrame
- [x] Filtering Data based on Condition
- [x] Filter Data with AND & OR Operations
- [x] `.set_index()` & `.reset_index()` in Pandas
- [x] Retrieve Row Values Using `loc` and `iloc` in Pandas
- [x] Set New/Multiple Values for a Specific Cell or Row
- [x] Rename Index Labels or Columns in Pandas
- [x] Delete Rows or Columns in Pandas
- [x] The `.nsmallest()` and `.nlargest()`, `.where()`, `.query()`, `.apply()` methods in Pandas

## 📖 Concepts

### Sorting algorithms
```python
df.sort_values("salary", ascending=False, na_position="first", kind="mergesort")
df.sort_values(["dept", "salary"], ascending=[True, False])
df.sort_index()
```
| `kind=` | Algorithm | Stable? | Notes |
|---|---|---|---|
| `quicksort` (default) | introsort | ❌ | fast on average |
| `mergesort` | merge / timsort | ✅ | keeps ties in their original order |
| `heapsort` | heapsort | ❌ | guaranteed $O(n \log n)$ |
| `stable` | radix / timsort | ✅ | same guarantee as mergesort |

`kind` only applies when sorting on **one** column. **Stable** means rows with equal keys keep their previous relative order, which is what makes multi-step sorting work.

### Filtering
```python
df[df["age"] > 30]
df[df["city"].isin(["Delhi", "Pune"])]
df[df["year"].between(2014, 2019)]
df[df["title"].str.contains("in", case=False)]
df[(df["dept"] == "Eng") & (df["salary"] > 80000)]   # AND
df[(df["city"] == "Delhi") | (df["age"] < 28)]        # OR
df[~df["paid"]]                                        # NOT
```
⚠️ Use `&`, `|` and `~`, never `and`, `or` or `not`. Wrap **each** condition in parentheses.

### Index management
`set_index("code")` turns a column into row labels, which makes `loc` lookups easy. `reset_index()` moves it back into a column, and `reset_index(drop=True)` renumbers from 0 after filtering.

### Getting and setting values
| | Label | Position |
|---|---|---|
| Rows/blocks | `df.loc[rows, cols]` (end included) | `df.iloc[rows, cols]` (end excluded) |
| One cell (fast) | `df.at[row, col]` | `df.iat[i, j]` |

```python
df.loc["P3", ["price", "stock"]] = [850, 20]          # several cells in one row
df.loc["P5"] = ["Lamp", 750, 10, "ok"]                # whole row / new row
df.loc[df["stock"] < 25, "status"] = "low stock"      # conditional update
```
Avoid chained assignment (`df[mask]["col"] = x`). It may change a temporary copy.

### Rename & delete
`rename(columns={...}, index={...})`, `rename(columns=str.lower)`, `add_prefix`, `rename_axis`. Delete with `drop(columns=/index=)`, `del df["c"]`, `df.pop("c")`, `dropna`, `drop_duplicates`, `truncate`.

### nlargest / nsmallest / where / query / apply
```python
df.nlargest(3, "runs")                       # top-3 rows
df["runs"].where(df["runs"] >= 500, 0)       # keep if True, else replace
df.query("team == 'MI' and runs > @min_runs")
df.apply(func, axis=1)                       # row-wise function
```

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `01_sorting_algorithms.py` | `sort_values`/`sort_index`, all four `kind=` algorithms, stability demo, timing on 1M rows, custom `key=` & categorical order |
| `02_filtering_data.py` | Boolean masks, comparison operators, `isin`, `between`, string & null conditions, `~`, `loc` filtering |
| `03_filter_and_or.py` | `&`, `\|`, `~`, mixing AND+OR, named masks, `query()` equivalents, common mistakes |
| `04_set_index_reset_index.py` | `set_index` (drop=False, MultiIndex), `reset_index` (drop=True, after groupby), `rename_axis` |
| `05_loc_iloc.py` | Rows, slices, cells and conditions with `loc` vs `iloc` |
| `06_setting_values.py` | `at`, `iat`, `loc`, `iloc` writes, whole rows, conditional updates, new rows/columns, the chained-assignment pitfall |
| `07_rename_labels_columns.py` | `rename` (dict/function), cleaning messy names, `set_axis`, `add_prefix/suffix`, `rename_axis` |
| `08_delete_rows_columns.py` | Deleting by name/position/dtype/NaN-share/condition, duplicates, `truncate`, `del`, `pop` |
| `09_nsmallest_nlargest_where_query_apply.py` | `nlargest`/`nsmallest` (ties), `where`, `query` with `@var`, `apply` on columns/rows |

## ▶️ How to Run
```bash
cd Week_3_Data_Analysis_with_Python/Module_5_Pandas_DataFrame_Continued
python 01_sorting_algorithms.py
python 02_filtering_data.py
# … through …
python 09_nsmallest_nlargest_where_query_apply.py
```

## 🧠 Key Takeaways
- Use a stable sort (`mergesort`/`stable`) when the order of ties matters.
- Boolean masks are the core of filtering. `query()` is a readable alternative.
- `loc` works with labels and includes the end; `iloc` works with positions and excludes it. Use `at`/`iat` for single cells.
- Write with `df.loc[mask, col] = value`, never with chained indexing.
- `nlargest(n, col)` is faster and clearer than `sort_values(...).head(n)`.

## 📝 Practice Exercises
1. Sort a table of students by class (ascending), then by marks (descending). Explain why a stable sort matters if you do it in two steps.
2. Filter orders that are from Delhi **or** Mumbai **and** unpaid, using both masks and `query()`.
3. `set_index("roll_no")` on a student table, update one student's marks with `.at`, then `reset_index()`.
4. Rename all columns to snake_case and drop any column that is more than 40% null.
5. Use `apply(axis=1)` to add a `grade` column, then show the 3 lowest scorers with `nsmallest`.
