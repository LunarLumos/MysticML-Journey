# 🧠 **Learning Notes: Handling Imbalanced Datasets in Machine Learning**

## 📌 **What is an Imbalanced Dataset?**

An **imbalanced dataset** occurs when the distribution of classes in a dataset is skewed. This means that one class (the **majority class**) has significantly more samples than another class (the **minority class**). In machine learning, this is a major issue because many algorithms assume that classes are equally represented, and they can perform poorly when that assumption is violated.

### **Example:**

For a binary classification problem, consider a dataset where:
- **Class 0 (Majority class)**: 9800 samples
- **Class 1 (Minority class)**: 200 samples

This means that for every 49 instances of Class 0, there is only 1 instance of Class 1.

---

## ❗ **Why is it a Problem?**

### **Model Bias:**
In an imbalanced dataset, the model tends to predict the majority class more frequently because it minimizes errors by favoring the class with more instances. As a result, the model's ability to predict the minority class accurately is diminished.

### **Impact on Evaluation Metrics:**
If we only look at accuracy, it can be misleading. A model that always predicts the majority class will have high accuracy, but it won't be useful if the minority class is more important. For instance:
- **In fraud detection**, predicting fraud correctly is more important than predicting legitimate transactions correctly.
- **In medical diagnoses**, predicting rare diseases correctly is crucial.

### **Common Metrics Affected by Imbalance:**
- **Accuracy:** High for majority class, misleading for minority class.
- **Precision, Recall, F1-Score:** Can be very low for the minority class.

### **Example:**
```python
from collections import Counter
print(Counter(y))
```
**Output:**
```text
Original class distribution: Counter({0: 9800, 1: 200})
```

In this example, we can immediately spot the imbalance, with the majority class (`0`) dominating the dataset.

---

## 🛠️ **How to Handle Imbalance: SMOTE (Synthetic Minority Over-sampling Technique)**

### **SMOTE** is a technique used to address imbalanced datasets by **generating synthetic samples** for the minority class. This process involves:
- **Creating new synthetic data points** for the minority class by interpolating between existing minority class samples.
- **Only applying SMOTE to the training set**, not the validation or test sets, to prevent data leakage and maintain model evaluation integrity.

### **How SMOTE Works:**
- The algorithm picks a sample from the minority class and finds its nearest neighbors.
- It then generates synthetic samples along the line joining the chosen sample and its neighbors.

By applying SMOTE, we balance the dataset by increasing the minority class samples while retaining the important patterns in the data.

**Example:**
Before SMOTE, the class distribution might look like this:
```text
Original class distribution: Counter({0: 9800, 1: 200})
```

After applying SMOTE to the training data, the distribution becomes balanced:
```text
Balanced class distribution: Counter({0: 6858, 1: 6858})
```

---

## 🔄 **Data Splitting Strategy**

To train and evaluate models in a realistic and fair way, we **split** the dataset into three parts:
- **70% for Training:** Used to train the model.
- **15% for Validation:** Used to tune hyperparameters.
- **15% for Testing:** Used to evaluate model performance on unseen data.

Using **Stratified Shuffle Split** ensures that the class proportions are preserved in each split. This is particularly important in imbalanced datasets to ensure the model gets a fair chance to learn both classes.

---

## 📊 **Visualizing the Class Distribution**

Visualizing the dataset before and after applying SMOTE is a great way to understand how class imbalance is handled.

1. **Class Distribution (Before SMOTE):**
   You can use a **bar plot** to visually check the distribution:
   ```python
   sns.countplot(data=df, x='target')
   ```

2. **Class Distribution (After SMOTE):**
   After applying SMOTE, the class distribution should look **balanced**:
   ```python
   sns.countplot(data=smote_df, x='target')
   ```

**Example:**
Before SMOTE:
```text
Original class distribution: 9800 samples of Class 0, 200 samples of Class 1.
```

After SMOTE:
```text
Balanced class distribution: 6858 samples of Class 0, 6858 samples of Class 1.
```

---

## ⚙️ **Training the Model and Evaluation**

We then train a **RandomForestClassifier** on the **balanced dataset** and evaluate it using several metrics:
- **Accuracy:** Overall performance on the test data.
- **Precision:** How many of the predicted positive samples were actually positive.
- **Recall:** How many of the actual positive samples were correctly predicted.
- **F1-Score:** The harmonic mean of precision and recall, providing a balance between them.

**Before SMOTE**:
```text
Accuracy: 1.00  
Recall for Class 1: Very Low (few minority class samples predicted correctly)
```

**After SMOTE**:
```text
Accuracy: 1.00  
Recall for Class 1: Much Higher (model correctly predicts more minority class samples)
```

---

## 📈 **Confusion Matrix and Precision-Recall Curve**

1. **Confusion Matrix:**
   This matrix shows the performance of the model by displaying:
   - **True Positives (TP):** Correctly predicted minority class samples.
   - **False Positives (FP):** Majority class samples incorrectly predicted as minority.
   - **True Negatives (TN):** Correctly predicted majority class samples.
   - **False Negatives (FN):** Minority class samples incorrectly predicted as majority.

2. **Precision-Recall Curve:**
   This curve is particularly useful for imbalanced datasets. It plots **precision vs recall**, allowing us to evaluate the trade-off between the two.

---

## 🧑‍💻 **My Learning Takeaways**

### **Key Points:**
1. **Imbalanced datasets can significantly affect model performance.**
2. **SMOTE** is an effective way to balance the dataset by generating synthetic samples for the minority class.
3. Always split your data into **train, validation, and test** sets to ensure proper model evaluation.
4. Visualizing the dataset before and after SMOTE helps you understand the impact of balancing the classes.
5. Model performance should be evaluated with metrics like **precision**, **recall**, and **f1-score**, not just **accuracy**.
   
> **Handling imbalanced datasets** is crucial for ensuring that your machine learning model gives **fair** and **reliable** predictions for all classes, especially when the minority class is important (e.g., rare diseases, fraud detection).

---
