import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_recall_curve,
    auc
)

# 1️⃣ Load Dataset
df = pd.read_csv('imbalanced_dataset.csv')
print("🔹 Dataset Shape:", df.shape)
print("🔹 Dataset Info:")
print(df.info())
print("\n🔹 Dataset Preview:")
print(df.head())

# Separate features and target
X = df.drop('label', axis=1)
y = df['label']

# 2️⃣ Visualize Original Class Distribution
print("\n🔹 Original Class Distribution:", Counter(y))
plt.figure(figsize=(6, 4))
sns.countplot(x=y)
plt.title("Original Class Distribution")
plt.xlabel("Class")
plt.ylabel("Count")
plt.show()

# 3️⃣ Split: 70% Train, 15% Validation, 15% Test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42
)

print("\n🔹 Dataset Split:")
print("Train set:", X_train.shape, Counter(y_train))
print("Validation set:", X_val.shape, Counter(y_val))
print("Test set:", X_test.shape, Counter(y_test))

# 4️⃣ SMOTE on Train Only
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)
print("\n🔹 After SMOTE on Train:", X_train_bal.shape, Counter(y_train_bal))

# Visualize Balanced Class Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x=y_train_bal)
plt.title("Balanced Class Distribution (Train After SMOTE)")
plt.xlabel("Class")
plt.ylabel("Count")
plt.show()

# 5️⃣ Train Classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train_bal, y_train_bal)

# 6️⃣ Evaluate on Validation Set
y_val_pred = clf.predict(X_val)
print("\n📊 Validation Set Report:")
print(classification_report(y_val, y_val_pred))

# 7️⃣ Evaluate on Test Set
y_test_pred = clf.predict(X_test)
print("\n📊 Test Set Report:")
print(classification_report(y_test, y_test_pred))

# 8️⃣ Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - Test Set")
plt.show()

# 9️⃣ Precision-Recall Curve
y_scores = clf.predict_proba(X_test)[:, 1]
precision, recall, _ = precision_recall_curve(y_test, y_scores)
pr_auc = auc(recall, precision)

plt.figure(figsize=(6, 4))
plt.plot(recall, precision, color='purple', label=f'PR AUC = {pr_auc:.2f}')
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve - Test Set")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
