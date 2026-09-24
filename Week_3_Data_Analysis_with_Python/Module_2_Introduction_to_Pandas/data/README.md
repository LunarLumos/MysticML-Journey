# data/ – sample files for Module 2

All files are **small, hand-written, synthetic** data (made-up names and numbers) created for this course.

| File | Format | Contents |
|---|---|---|
| `employees.csv` | Comma-separated, header row | 15 employees: `emp_id, name, department, city, age, salary, join_date, rating`. One missing `salary` (Vikram) and one missing `rating` (Ananya) on purpose, for cleaning practice. |
| `employees.txt` | Pipe (`\|`) separated text, header row | 5 more employees with `emp_id, name, department, city, age, salary` (read with `sep="|"`). |
| `notes.txt` | Plain text | 3 free-text lines, to show reading an unstructured `.txt` file. |

Used by `02_pandas_for_data_analysis.py`, `04_reading_csv_txt.py` and `05_reading_from_database.py` (which loads the CSV into an in-memory SQLite database).
