# Polynomial Regression

## **What is Polynomial Regression?**

**Polynomial Regression** is an extension of **Multiple Linear Regression** where we introduce polynomial terms (squared, cubic, etc.) to capture **non-linear** relationships between the independent variables (features) and the dependent variable (target).

The general formula for a **second-degree polynomial regression** (quadratic) is:

```
Y = β₀ + β₁X + β₂X² + ε
```

For **multiple features**, it extends to:

```
Y = β₀ + β₁X₁ + β₂X₁² + β₃X₂ + β₄X₂² + ... + βnXn² + ε
```

Where:
- **Y** = Dependent variable (e.g., house price)
- **β₀** = Intercept
- **β₁, β₂, ... βn** = Coefficients of features
- **X₁, X₂, ... Xn** = Independent variables (predictors, e.g., area, bedrooms)
- **X², X³** = Squared, cubic terms (to capture non-linearity)
- **ε** = Error term

---

## **📌 When to Use Polynomial Regression?**

Use **Polynomial Regression** when:
- The relationship between the **independent variables and target is non-linear**.
- A straight-line model (**Multiple Linear Regression**) does not fit the data well.
- The data exhibits **curved trends** (e.g., house prices rising faster for luxury homes).

---

## **📊 Real-life Example: House Price Prediction**

Consider this dataset where house prices increase **non-linearly** with area:

| **Area (sq. ft.)** | **Bedrooms** | **Age (years)** | **Price (in $1000)** |
|--------------------|--------------|-----------------|----------------------|
| 800               | 2            | 40              | 80                   |
| 1000              | 3            | 35              | 120                  |
| 1500              | 3            | 25              | 170                  |
| 2000              | 4            | 20              | 250                  |
| 3000              | 5            | 10              | 400                  |
| 4000              | 6            | 5               | 600                  |

Here, price doesn’t increase linearly with area—**it accelerates!**

---

## **🔄 Applying Polynomial Regression to the House Price Dataset**

Since prices **increase exponentially** for luxury homes, we introduce a squared term (**Area²**) in the equation:

```
Price = β₀ + β₁ * Area + β₂ * Area² + β₃ * Bedrooms + β₄ * Age
```

---

## **Steps in Polynomial Regression**

### **1️⃣ Calculate the Coefficients**

Assume we trained a **Polynomial Regression Model**, and got these coefficients:

- β₀ = 50,000 (intercept)
- β₁ = 80 (coefficient for area)
- β₂ = 0.02 (coefficient for area²)
- β₃ = -15,000 (coefficient for bedrooms)
- β₄ = -10,000 (coefficient for age)

### **2️⃣ Regression Equation**

```
Price = 50,000 + 80 * Area + 0.02 * Area² - 15,000 * Bedrooms - 10,000 * Age
```

### **3️⃣ Prediction for a New House**

We predict the price of a **2,500 sq. ft.**, 4-bedroom, 15-year-old house:

```
Price = 50,000 + 80(2500) + 0.02(2500²) - 15,000(4) - 10,000(15)
```

```
Price = 50,000 + 200,000 + 125,000 - 60,000 - 150,000
```

```
Price = 165,000
```

🛠 **Compared to Multiple Linear Regression, this model fits the increasing house price trend better.**

---

## **📉 Key Difference: Multiple Linear Regression vs. Polynomial Regression**

| Feature | Multiple Linear Regression | Polynomial Regression |
|---------|---------------------------|----------------------|
| **Equation** | Uses only original features | Adds squared, cubic terms |
| **Graph Shape** | Straight Line 📈 | Curved Line 🔄 |
| **Feature Relationship** | Linear (constant effect) | Non-linear (effect changes) |
| **Example in Real Estate** | Price increases at a fixed rate per sq. ft. | Price rises faster for larger homes |

---

## **📌 Conclusion**

- **Use Multiple Linear Regression** if your data follows a **straight-line trend**.
- **Use Polynomial Regression** when the data has **curves or accelerating patterns**.

🏡 **For real estate prices, polynomial regression often works better because high-value properties increase exponentially in price.** 🚀

