# Module 4 – Pandas (DataFrame)
> Week 3 · Data Analysis with Python   |   ⬅ Previous: [Module 3 – Pandas Series](../Module_3_Pandas_Series)  ·  Next ➡: [Module 5 – DataFrame Continued](../Module_5_Pandas_DataFrame_Continued)

## 🎯 Learning Objectives
- Explain what a DataFrame is and create one from dicts, lists, arrays, Series and files
- Explore a DataFrame with its most useful functions (`info`, `describe`, `groupby`, `corr`, …)
- Select subsets of columns, add new columns and drop rows or columns
- Use broadcasting and handle null values by dropping or filling them

## ✅ Syllabus Checklist
- [x] What is DataFrame and its use | Creating DataFrame
- [x] DataFrame different functions
- [x] Dropping columns/rows from DataFrame
- [x] Display Particular Columns from DataFrame (Subset of DataFrame)
- [x] Add New Column to DataFrame
- [x] Broadcasting Operations in DataFrame | Dropping and Filling Null Values

## 📖 Concepts

### What is a DataFrame?
A 2-D labelled table: **index** (row labels) × **columns**, where every column is a Series with its own dtype. It's the pandas equivalent of a SQL table or an Excel sheet.

### Creating DataFrames
| Source | Code |
|---|---|
| dict of lists | `pd.DataFrame({"a": [1, 2], "b": [3, 4]})` |
| list of dicts | `pd.DataFrame([{"a": 1}, {"a": 2, "b": 5}])` |
| list of lists | `pd.DataFrame(rows, columns=[...])` |
| NumPy array | `pd.DataFrame(arr, index=..., columns=...)` |
| file | `pd.read_csv(...)` |

### Must-know functions
`head`, `tail`, `sample`, `shape`, `dtypes`, `info()`, `describe()`, `nunique()`, `value_counts()`, `mean(axis=0/1)`, `groupby().agg()`, `corr()`, `copy()`, `astype()`.

### Selecting columns
```python
df["name"]              # Series
df[["name", "age"]]     # DataFrame (note the double brackets)
df.filter(like="salary")
df.select_dtypes(include="number")
df.loc[:, "name":"city"]
```

### Adding & dropping
```python
df["total"] = df["qty"] * df["price"]                 # computed column
df["big"] = np.where(df["total"] > 100, "yes", "no")  # conditional column
df.insert(0, "id", range(len(df)))                    # at a position
df = df.assign(tax=lambda d: d.total * 0.18)          # chaining
df = df.drop(columns=["tmp"])                         # drop a column
df = df.drop(index=[0, 3])                            # drop rows
```

### Broadcasting
A scalar or Series is stretched to match the DataFrame. `df * 1.18` updates every cell. `df - series` aligns on **column** labels, and `df.mul(series, axis=0)` aligns on **row** labels.

### Null values
| Goal | Code |
|---|---|
| count | `df.isna().sum()` |
| drop rows with any null | `df.dropna()` |
| only if a column is null | `df.dropna(subset=["name"])` |
| keep rows with ≥ n values | `df.dropna(thresh=n)` |
| fill per column | `df.fillna({"age": df.age.median(), "city": "Unknown"})` |
| carry forward / back | `df.ffill()`, `df.bfill()` |

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `01_creating_dataframe.py` | Seven ways to build a DataFrame, and why to use one |
| `02_dataframe_functions.py` | Inspection, structure attributes, row/column stats, groupby/agg, corr, copy, astype |
| `03_dropping_rows_columns.py` | `drop` by label/position/condition, `errors='ignore'`, `inplace`, `del`, `pop` |
| `04_subset_columns.py` | Single vs double brackets, `filter`, `select_dtypes`, `loc`/`iloc` column slices |
| `05_add_new_column.py` | Constant/list/computed/`np.where`/`map`/`apply` columns, `insert`, `assign`, `pd.cut`, adding a row |
| `06_broadcasting_and_null_values.py` | Scalar & Series broadcasting (both axes), `isna`, `dropna` variants, `fillna`, `ffill`, `bfill`, `interpolate` |

## ▶️ How to Run
```bash
cd Week_3_Data_Analysis_with_Python/Module_4_Pandas_DataFrame
python 01_creating_dataframe.py
python 02_dataframe_functions.py
python 03_dropping_rows_columns.py
python 04_subset_columns.py
python 05_add_new_column.py
python 06_broadcasting_and_null_values.py
```

## 🧠 Key Takeaways
- `df["col"]` returns a Series and `df[["col"]]` returns a DataFrame.
- Most methods return a **new** DataFrame. Re-assign the result (`df = df.drop(...)`) instead of relying on `inplace=True`.
- Vectorised column maths and `np.where` are faster and clearer than loops.
- Choose a null strategy per column: numeric columns get the median or mean, categorical columns get the mode or "Unknown".

## 📝 Practice Exercises
1. Build a DataFrame of 6 products (name, category, price, stock) and print only the columns with numeric data.
2. Add `stock_value = price * stock` and a `status` column that says "reorder" when stock < 10.
3. Drop every product in one category, then drop the `category` column.
4. Insert some `NaN` values, then fill numeric columns with their median and text columns with "Unknown".
5. Increase every price by 5% with broadcasting and round the result to 2 decimals.
