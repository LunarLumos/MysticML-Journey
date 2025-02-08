# Single Linear Regression

### **What is Single Linear Regression?**

**Single Linear Regression** models the relationship between an independent variable (X) and a dependent variable (Y) by fitting a straight line:

$$
Y = mX + c
$$

Where:
- **Y** = Dependent variable (e.g., house price)
- **X** = Independent variable (e.g., area in sq. ft.)
- **m** = Slope (coefficient)
- **c** = Intercept

### **When to Use Single Linear Regression**

Use **Single Linear Regression** when:
- There is a **linear relationship** between the predictor and the target
- You have **one predictor** affecting the outcome
- You’re predicting a **continuous variable**

### **Real-life Example: House Price Prediction**

| **Area (sq. ft.)** | **Price (in $1000)** |
|--------------------|----------------------|
| 1500               | 300                  |
| 1800               | 330                  |
| 2400               | 400                  |
| 3000               | 475                  |
| 3500               | 520                  |
| 4000               | 600                  |

#### **Applying Single Linear Regression to the House Price Dataset:**

1. **Calculate sums:**

$$
\sum{X} = 15100, \quad \sum{Y} = 2625, \quad \sum{X_i Y_i} = 11115000, \quad \sum{X^2} = 37215000
$$

2. **Find slope (m) and intercept (c):**

$$
m = 0.1122, \quad c = 87.16
$$

3. **Regression equation:**

$$
Y = 0.1122X + 87.16
$$

4. **Prediction for 2500 sq. ft. house:**

We have the regression equation:

$$
Y = 0.1122X + 87.16
$$

For \( X = 2500 \) (area in square feet), we substitute \( X = 2500 \) into the equation:

$$
Y = 0.1122 \times 2500 + 87.16
$$

$$
Y = 280.5 + 87.16
$$
$$
Y = 367.66 
$$


Thus, the **correct predicted price** for a **2500 sq. ft.** house is **$367.660**.

---

### **Conclusion**

**Single Linear Regression** is used when there’s a linear relationship between a single predictor and a target, making it ideal for simple predictions like house prices based on area.
