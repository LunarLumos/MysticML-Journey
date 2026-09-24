
# Multiple Linear Regression

### **What is Multiple Linear Regression?**

**Multiple Linear Regression (MLR)** is an extension of Simple Linear Regression that models the relationship between two or more independent variables and a dependent variable by fitting a linear equation to the observed data. The general formula is:

```
Y = β₀ + β₁X₁ + β₂X₂ + ... + βnXn + ε
```

Where:
- **Y** = Dependent variable (target, e.g., house price)
- **β₀** = Intercept (the value of Y when all Xᵢ = 0)
- **β₁, β₂, ... βn** = Coefficients (slopes) of the features X₁, X₂, ... Xn
- **X₁, X₂, ... Xn** = Independent variables (predictors, e.g., area, number of bedrooms)
- **ε** = Error term (random noise)

### **When to Use Multiple Linear Regression**

Use **Multiple Linear Regression** when:
- There is a **linear relationship** between the predictors and the target.
- You have **multiple predictors** influencing the target.
- You’re predicting a **continuous variable**.

### **Real-life Example: House Price Prediction**

| **Area (sq. ft.)** | **Bedrooms** | **Age (years)** | **Price (in $1000)** |
|--------------------|--------------|-----------------|----------------------|
| 1500               | 3            | 10              | 350                  |
| 1800               | 4            | 5               | 420                  |
| 2400               | 3            | 15              | 460                  |
| 3000               | 5            | 20              | 580                  |
| 2200               | 4            | 8               | 500                  |

#### **Applying Multiple Linear Regression to the House Price Dataset:**

The equation for predicting the price of a house would be:

```
Price = β₀ + β₁ * Area + β₂ * Bedrooms + β₃ * Age
```

### **Steps in Multiple Linear Regression:**

1. **Calculate the coefficients:**
   After training the model, we get the coefficients for the features (area, bedrooms, age). Let’s assume the following coefficients from a trained model:
   - β₀ = 200,000 (intercept)
   - β₁ = 100 (coefficient for area)
   - β₂ = -20,000 (coefficient for bedrooms)
   - β₃ = -15,000 (coefficient for age)

2. **Regression equation:**

   Using the coefficients, the regression equation is:

```
Price = 200,000 + 100 * Area - 20,000 * Bedrooms - 15,000 * Age
```

3. **Prediction for a new house:**

   Suppose we want to predict the price of a house with the following features:
   - Area = 2000 sq. ft.
   - Bedrooms = 4
   - Age = 10 years

   Substituting these values into the regression equation:

```
Price = 200,000 + 100 * 2000 - 20,000 * 4 - 15,000 * 10
```

Simplifying:

```
Price = 200,000 + 200,000 - 80,000 - 150,000
```

```
Price = 170,000
```

So, the predicted price for this house is **$170,000**.

---

### **Conclusion**

**Multiple Linear Regression** is useful when you have more than one predictor influencing the target variable. By fitting a linear model to the data, you can make predictions based on multiple features, such as house prices based on area, number of bedrooms, and age.

---
