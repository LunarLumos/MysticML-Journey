import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Load the CSV file
data = pd.read_csv("house_prices.csv")

# Check the number of data points in the dataset
print(f"{Fore.GREEN}[*] Total number of data points: {data.shape[0]}")

# Check for null values and data types
print(f"\n{Fore.YELLOW}[+] Data Types:\n", data.dtypes)
print(f"\n{Fore.YELLOW}[+] Missing Values:\n", data.isnull().sum())

# Check if the dataset contains any missing values or problematic data
if data.isnull().sum().any():
    print(f"{Fore.RED}[!] Dataset contains missing values. Consider filling or dropping them.")
    # Optionally, handle missing values (e.g., drop rows or fill with mean/median)
    data = data.dropna()  # This drops rows with any missing values
    # or
    # data.fillna(data.mean(), inplace=True)  # This fills missing values with the column mean
    print(f"{Fore.GREEN}[*] Missing values have been handled.")

# Check if the essential columns exist
required_columns = ['Area', 'Price']
if not all(col in data.columns for col in required_columns):
    print(f"{Fore.RED}[!] Dataset is missing one or more required columns: {required_columns}")
    exit()

# Extract features (X) and target variable (Y)
X = data[['Area']]  # Independent variable
Y = data['Price']   # Dependent variable

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, Y_train)

# Make predictions
Y_pred = model.predict(X_test)

# Model evaluation
mae = mean_absolute_error(Y_test, Y_pred)
mse = mean_squared_error(Y_test, Y_pred)
rmse = np.sqrt(mse)
r2_score = model.score(X_test, Y_test)  # R-squared (coefficient of determination)

# Output evaluation metrics
print(f"\n{Fore.GREEN}[*] Model Evaluation:")
print(f"{Fore.CYAN}[+] Mean Absolute Error: {mae:.2f}")
print(f"{Fore.CYAN}[+] Mean Squared Error: {mse:.2f}")
print(f"{Fore.CYAN}[+] Root Mean Squared Error: {rmse:.2f}")
print(f"{Fore.CYAN}[+] R-squared (Accuracy): {r2_score:.2f} \n")

# Explanation of R-squared value
if r2_score == 1:
    print(f"{Fore.GREEN}[*] R-squared = 1 means perfect fit! The model explains all the variance in the target variable.")
elif r2_score > 0.85:
    print(f"{Fore.YELLOW}[+] R-squared is quite high: {r2_score:.2f}, meaning the model fits the data well!")
else:
    print(f"{Fore.RED}[!] R-squared is low: {r2_score:.2f}, meaning the model doesn't explain much of the variance.")

# Model parameters: Slope and Intercept
print(f"\n{Fore.GREEN}[*] Model Parameters:")
print(f"{Fore.MAGENTA}[+] Slope (Coefficient for Area): {model.coef_[0]:.2f}")
print(f"{Fore.MAGENTA}[+] Intercept (Price when Area = 0): {model.intercept_:.2f}")

# Predict price for a new house with 1900 sq. ft. area
new_area = np.array([[1900]])
predicted_price = model.predict(new_area)
print(f"\n{Fore.GREEN}[*] Predicted price for 1900 sq. ft. house: ${predicted_price[0]:,.2f}")

# Visualization
X_sorted = np.sort(X.values, axis=0)  # Sorting X values to display the regression line correctly
plt.scatter(X, Y, color='blue', label="Actual Data")
plt.plot(X_sorted, model.predict(X_sorted), color='red', linewidth=2, label="Regression Line")
plt.xlabel("Area (sq. ft.)")
plt.ylabel("Price (USD)")
plt.title("Single Linear Regression - House Price Prediction")
plt.legend()
plt.show()
