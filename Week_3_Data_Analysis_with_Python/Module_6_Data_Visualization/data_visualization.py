import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for Seaborn
sns.set_style("darkgrid")

# 1️⃣ Line Plot
x = np.linspace(0, 10, 100)  # 100 values between 0 and 10
y = np.sin(x)  # Sine function

plt.figure(figsize=(6, 4))
plt.plot(x, y, label="Sine Wave", color="blue", linestyle="--")
plt.title("Line Plot Example")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.show()

# 2️⃣ Bar Chart
categories = ['A', 'B', 'C', 'D']
values = [10, 20, 15, 25]

plt.figure(figsize=(6, 4))
plt.bar(categories, values, color='green')
plt.title("Bar Chart Example")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.show()

# 3️⃣ Histogram
data = np.random.randn(1000)  # 1000 random values

plt.figure(figsize=(6, 4))
plt.hist(data, bins=30, color='purple', edgecolor='black')
plt.title("Histogram Example")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

# 4️⃣ Scatter Plot
x = np.random.rand(50)
y = np.random.rand(50)

plt.figure(figsize=(6, 4))
plt.scatter(x, y, color='red')
plt.title("Scatter Plot Example")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()

# 5️⃣ Box Plot (Using Seaborn)
data = np.random.randn(100)

plt.figure(figsize=(6, 4))
sns.boxplot(data=data)
plt.title("Box Plot Example")
plt.show()

# 6️⃣ Heatmap (Using Seaborn)
matrix = np.random.rand(5, 5)  # 5x5 random matrix

plt.figure(figsize=(6, 4))
sns.heatmap(matrix, annot=True, cmap="coolwarm")
plt.title("Heatmap Example")
plt.show()
