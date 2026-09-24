# Week 3 – Data Analysis with Python 🐍📊

> ⬅ Previous: [Week 2 – Data Analysis with MySQL](../Week_2_Data_Analysis_with_MySQL)  ·  Next ➡: [Week 4 – Machine Learning](../Week_4_Machine_Learning)

## Overview
In Week 2 we asked questions of data with SQL. This week we do the same, and more, in Python. Every ML project in Week 4 starts with the same steps: **load the data, clean it, explore it, and visualise it.** The tools for that are NumPy (fast numeric arrays), pandas (labelled tables) and Matplotlib/Seaborn (charts).

Each module has small numbered scripts, one topic per script. Every script runs offline with `python <file>.py` and prints clearly labelled sections.

## Modules
| # | Module | What you'll learn |
|---|---|---|
| 1 | [NumPy](Module_1_NumPy) | ndarrays, creating arrays, indexing & slicing, broadcasting, maths & matrix operations, random numbers |
| 2 | [Introduction to Pandas](Module_2_Introduction_to_Pandas) | Why pandas, Series vs DataFrame, reading CSV/TXT files and SQL databases (SQLite in memory + MySQL variant) |
| 3 | [Pandas Series](Module_3_Pandas_Series) | Creating Series, Series vs list, functions & sorting, extracting values, `value_counts`, `apply`, duplicates & missing values |
| 4 | [Pandas DataFrame](Module_4_Pandas_DataFrame) | Creating DataFrames, key functions, subsets, adding & dropping columns/rows, broadcasting, null handling |
| 5 | [DataFrame Continued](Module_5_Pandas_DataFrame_Continued) | Sorting algorithms, filtering with `&`/`\|`, `set_index`/`reset_index`, `loc`/`iloc`/`at`/`iat`, rename, delete, `nlargest`/`where`/`query`/`apply` |
| 6 | [Data Visualization](Module_6_Data_Visualization) | Line, scatter, bar, histogram, pie and box plots, outlier detection (IQR & Z-score), heatmaps |

## Prerequisites
- Week 1 Python basics: variables, lists, dicts, loops, functions, comprehensions
- Week 2 SQL: `SELECT`, `WHERE`, `GROUP BY` and `JOIN` map directly onto pandas filtering, `groupby` and `merge`

## Setup
```bash
# from the repo root (Python 3.10+)
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install numpy pandas matplotlib seaborn scipy scikit-learn
# optional, for the MySQL example in Module 2:
pip install sqlalchemy mysql-connector-python
```
Run any script from inside its module folder:
```bash
cd Week_3_Data_Analysis_with_Python/Module_1_NumPy
python 01_numpy_introduction.py
```
Plots are saved to each module's `outputs/` folder (git-ignored). On a server without a display, use `MPLBACKEND=Agg python <script>.py`.

Tested with Python 3.11, NumPy 2.4, pandas 3.0, Matplotlib 3.11 and Seaborn 0.13.

## Data used this week
- `Module_2_Introduction_to_Pandas/data/`: small **synthetic** employee CSV/TXT files (see [data/README.md](Module_2_Introduction_to_Pandas/data/README.md))
- Most other scripts build small **synthetic, seeded** DataFrames inside the script, so no downloads are needed
- `Module_6/09_heatmap.py` uses scikit-learn's bundled **Iris** dataset (works offline)

## Original files
The learner's first-pass scripts are kept next to the new material: `Module_1_NumPy/numpy_basics.py`, `Module_2_Introduction_to_Pandas/pandas_intro.py` and `Module_6_Data_Visualization/data_visualization.py`.

## How this connects to Week 4
Week 4 (Machine Learning) assumes you can:
- load a dataset into a DataFrame and split it into features `X` and target `y` (Modules 2, 4, 5)
- find and fix missing values, duplicates and outliers (Modules 3, 4, 6)
- explore relationships with scatter plots and correlation heatmaps (Module 6)
- use NumPy arrays, which is what scikit-learn models take as input (Module 1)
