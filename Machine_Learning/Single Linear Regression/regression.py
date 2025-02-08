import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load the CSV file
data = pd.read_csv("house_prices.csv")

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

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")

# Predict price for a new house with 1900 sq. ft. area
new_area = np.array([[1900]])
predicted_price = model.predict(new_area)
print(f"Predicted price for 1900 sq. ft. house: ${predicted_price[0]:,.2f}")

# Visualization
plt.scatter(X, Y, color='blue', label="Actual Data")
plt.plot(X, model.predict(X), color='red', linewidth=2, label="Regression Line")
plt.xlabel("Area (sq. ft.)")
plt.ylabel("Price (USD)")
plt.title("Single Linear Regression - House Price Prediction")
plt.legend()
plt.show()
