import pandas as pd

# 1️⃣ Creating a Pandas Series (1D Data)
data = [10, 20, 30, 40, 50]
series = pd.Series(data, index=['A', 'B', 'C', 'D', 'E'])
print("Pandas Series:\n", series)

# Accessing elements
print("Value at index 'C':", series['C'])
print("Mean of Series:", series.mean())

# 2️⃣ Creating a Pandas DataFrame (2D Data)
data = {
    'Name': ['Aadil', 'Yaana', 'Sama', 'lilith'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Paris', 'London', 'Tokyo'],
    'Salary': [50000, 60000, 70000, 80000]
}

df = pd.DataFrame(data)
print("\nPandas DataFrame:\n", df)

# 3️⃣ Basic DataFrame Operations
print("\nColumn Names:", df.columns)
print("Shape of DataFrame:", df.shape)
print("\nFirst 2 Rows:\n", df.head(2))  # First 2 rows
print("\nLast 2 Rows:\n", df.tail(2))  # Last 2 rows
print("\nSummary Statistics:\n", df.describe())  # Statistical summary

# 4️⃣ Selecting Data
print("\nAccessing 'Name' Column:\n", df['Name'])
print("\nAccessing First Row using iloc:\n", df.iloc[0])
print("\nAccessing 'Name' and 'City' Columns:\n", df[['Name', 'City']])

# 5️⃣ Filtering Data
print("\nPeople Older than 30:\n", df[df['Age'] > 30])
print("\nPeople in London:\n", df[df['City'] == 'London'])

# 6️⃣ Adding a New Column
df['Bonus'] = df['Salary'] * 0.10  # 10% bonus on salary
print("\nDataFrame with Bonus Column:\n", df)

# 7️⃣ Sorting Data
print("\nSorted by Age:\n", df.sort_values(by='Age', ascending=False))

# 8️⃣ Grouping Data
grouped = df.groupby('City')['Salary'].mean()
print("\nAverage Salary by City:\n", grouped)

# 9️⃣ Handling Missing Data
df.loc[2, 'Salary'] = None  # Introducing a missing value
print("\nDataFrame with Missing Value:\n", df)
print("\nDropping Rows with Missing Values:\n", df.dropna())
print("\nFilling Missing Values with 0:\n", df.fillna(0))
