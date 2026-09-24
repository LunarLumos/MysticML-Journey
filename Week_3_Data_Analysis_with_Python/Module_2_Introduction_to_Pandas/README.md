# Module 2 – Introduction to Pandas for Data Analysis
> Week 3 · Data Analysis with Python   |   ⬅ Previous: [Module 1 – NumPy](../Module_1_NumPy)  ·  Next ➡: [Module 3 – Pandas Series](../Module_3_Pandas_Series)

## 🎯 Learning Objectives
- Install pandas and understand where it fits (built on NumPy)
- Follow the typical analysis workflow: load → inspect → clean → transform → analyse
- Tell a Series from a DataFrame and convert between them
- Read data from CSV files, delimited/plain TXT files and SQL databases

## ✅ Syllabus Checklist
- [x] Installing Pandas | Pandas Introduction
- [x] Use of Pandas for Data Analysis
- [x] Series vs DataFrames
- [x] Reading data from CSV and TXT file and databases

## 📖 Concepts

### Installing & importing
```bash
pip install pandas            # optional for the MySQL variant: pip install sqlalchemy mysql-connector-python
```
```python
import pandas as pd
```

### Why pandas?
NumPy is great for numbers in a grid; real data has **labels, mixed types and missing values**. pandas adds labelled rows/columns, handles `NaN`, and gives SQL-like tools (`groupby`, `merge`, `pivot_table`) plus readers/writers for CSV, Excel, JSON and SQL.

### Series vs DataFrame
| | Series | DataFrame |
|---|---|---|
| Dimensions | 1-D | 2-D |
| Think of it as | one column | a whole table / spreadsheet |
| Labels | index | index **and** columns |
| `df["col"]` | – | returns a Series |
| `df[["col"]]` | – | returns a DataFrame |

### Reading files
```python
pd.read_csv("data/employees.csv")                       # CSV
pd.read_csv("data/employees.csv", usecols=[...], index_col="emp_id",
            parse_dates=["join_date"], nrows=5)          # useful options
pd.read_csv("data/employees.txt", sep="|")              # delimited TXT
df.to_csv("outputs/out.csv", index=False)               # write back
```

### Reading from databases
`pd.read_sql_query(sql, connection)` turns any `SELECT` into a DataFrame, and `df.to_sql(name, connection)` writes one. The script uses **SQLite in memory** (built into Python, no server needed). The same code works against the MySQL databases from Week 2 through SQLAlchemy:
```python
from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/join_demo")
df = pd.read_sql("SELECT * FROM students", engine)
```
Always pass user values as `params=` (never build SQL strings with f-strings) to avoid SQL injection.

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `pandas_intro.py` | The learner's original tour: Series, DataFrame, selection, filtering, new columns, sorting, groupby, missing data |
| `01_pandas_introduction.py` | Install/version check, first Series & DataFrame, display options |
| `02_pandas_for_data_analysis.py` | End-to-end mini analysis of `employees.csv` (inspect, clean, transform, groupby, pivot) |
| `03_series_vs_dataframe.py` | Attribute comparison table, converting between Series and DataFrame |
| `04_reading_csv_txt.py` | `read_csv` options, pipe-delimited and plain `.txt`, writing CSV/TSV to `outputs/` |
| `05_reading_from_database.py` | SQLite in-memory DB: `to_sql`, `read_sql_query`, GROUP BY, parameters, JOIN; commented MySQL variant |
| `data/` | Sample CSV/TXT files (see [data/README.md](data/README.md)) |

## ▶️ How to Run
```bash
cd Week_3_Data_Analysis_with_Python/Module_2_Introduction_to_Pandas
python 01_pandas_introduction.py
python 02_pandas_for_data_analysis.py
python 03_series_vs_dataframe.py
python 04_reading_csv_txt.py      # writes outputs/engineering.csv & .txt
python 05_reading_from_database.py
python pandas_intro.py
```

## 🧠 Key Takeaways
- A DataFrame is a collection of Series that share one index.
- `read_csv` handles far more than commas: `sep`, `usecols`, `index_col`, `parse_dates`, `dtype`, `nrows`.
- SQL and pandas work together: filter or aggregate in SQL, finish the analysis in pandas.
- Always look at your data (`head`, `info`, `describe`, `isna().sum()`) before analysing it.

## 📝 Practice Exercises
1. Load `employees.csv` and find the city with the highest average rating.
2. Read `employees.txt`, combine it with the CSV using `pd.concat`, and save the result to `outputs/all_employees.csv`.
3. In the SQLite script, write a query that returns employees who joined before 2018, ordered by salary.
4. Convert the `salary` column of a DataFrame into a Series, then back into a one-column DataFrame.
