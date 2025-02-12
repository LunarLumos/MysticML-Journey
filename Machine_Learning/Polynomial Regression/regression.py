import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Load the dataset
data = pd.read_csv('house_prices_multiple.csv')

# Check dataset info
print(f"{Fore.GREEN}[*] Total number of data points: {data.shape[0]}")
print(f"\n{Fore.YELLOW}[+] Data Types:\n", data.dtypes)
print(f"\n{Fore.YELLOW}[+] Missing Values:\n", data.isnull().sum())

# Handle missing values (drop rows)
if data.isnull().sum().any():
    print(f"{Fore.RED}[!] Missing values detected. Handling them now...")
    data = data.dropna()
    print(f"{Fore.GREEN}[*] Missing values have been removed.")

# Ensure required columns exist
required_columns = ['Area', 'Bedrooms', 'Age', 'Price']
if not all(col in data.columns for col in required_columns):
    print(f"{Fore.RED}[!] Dataset missing required columns: {required_columns}")
    exit()

# Extract features (X) and target variable (Y)
X = data[['Area', 'Bedrooms', 'Age']]
Y = data['Price']

# Split data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Convert features to polynomial (degree=2 for curved fitting)
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Train Polynomial Regression model
model = LinearRegression()
model.fit(X_train_poly, Y_train)

# Make predictions
Y_pred = model.predict(X_test_poly)

# Model evaluation
mae = mean_absolute_error(Y_test, Y_pred)
mse = mean_squared_error(Y_test, Y_pred)
rmse = np.sqrt(mse)
r2_score = model.score(X_test_poly, Y_test)

# Output evaluation metrics
print(f"\n{Fore.GREEN}[*] Model Evaluation:")
print(f"{Fore.CYAN}[+] Mean Absolute Error: {mae:.2f}")
print(f"{Fore.CYAN}[+] Mean Squared Error: {mse:.2f}")
print(f"{Fore.CYAN}[+] Root Mean Squared Error: {rmse:.2f}")
print(f"{Fore.CYAN}[+] R-squared (Accuracy): {r2_score:.2f} \n")

# Explain R-squared
if r2_score == 1:
    print(f"{Fore.GREEN}[*] Perfect fit! The model explains all the variance.")
elif r2_score > 0.85:
    print(f"{Fore.YELLOW}[+] Model fits well (R² = {r2_score:.2f})!")
else:
    print(f"{Fore.RED}[!] Model may not explain much of the variance.")

# Predict price for a new house
new_data = np.array([[1900, 4, 10]])  # 1900 sqft, 4 bedrooms, 10 years old
new_data_poly = poly.transform(new_data)
predicted_price = model.predict(new_data_poly)
print(f"\n{Fore.GREEN}[*] Predicted price for 1900 sq. ft., 4 bedrooms, 10 years old house: ${predicted_price[0]:,.2f}")

# Visualization (for Area vs Price)
plt.scatter(data['Area'], data['Price'], color='blue', label="Actual Data")
plt.xlabel("Area (sq. ft.)")
plt.ylabel("Price (USD)")
plt.title("Polynomial Regression - House Price Prediction")

# Generate a smooth curve for visualization
X_curve = np.linspace(min(data['Area']), max(data['Area']), 100).reshape(-1, 1)
X_curve_poly = poly.transform(np.column_stack((X_curve, np.ones_like(X_curve), np.ones_like(X_curve))))  # Keeping other variables constant
Y_curve = model.predict(X_curve_poly)

plt.plot(X_curve, Y_curve, color='red', linewidth=2, label="Polynomial Regression Curve")
plt.legend()
plt.show()
