# Module 5 – Model Performance Metrics
> Week 6 · Deep Learning   |   ⬅ Previous: [Module 4 – Introduction to RNN](../Module_4_Introduction_to_RNN)  ·  Next ➡: [Projects](../../Projects)

## 🎯 Learning Objectives
- Read a confusion matrix and compute precision, recall and F1 by hand.
- Choose a decision threshold based on the cost of false positives versus false negatives.
- Spot underfitting and overfitting using train/validation scores and learning curves, and fix overfitting (Dropout, L2, EarlyStopping).
- Understand how the learning rate and batch size affect training.
- Know why feature scaling matters and how to do it without data leakage.
- Detect and handle outliers.

## ✅ Syllabus Checklist
- [x] Confusion Matrix
- [x] Precision Score | Recall Score | F1 – Score
- [x] Overfitting and Underfitting
- [x] Learning rate | Batch Size
- [x] Feature Scaling
- [x] Outliers

## 📖 Concepts

### Confusion matrix
|  | Predicted negative | Predicted positive |
|---|---|---|
| **Actual negative** | TN | FP (Type I, false alarm) |
| **Actual positive** | FN (Type II, missed) | TP |

sklearn's `confusion_matrix` prints `[[TN, FP], [FN, TP]]`.

### Precision, recall, F1
$$ \text{Precision} = \frac{TP}{TP+FP} \quad \text{Recall} = \frac{TP}{TP+FN} \quad F_1 = 2\cdot\frac{P\cdot R}{P+R} $$
- **Precision:** "When I say positive, how often am I right?" This matters when false alarms are costly (spam filters).
- **Recall:** "Of all real positives, how many did I catch?" This matters when misses are costly (cancer screening).
- **F1:** the harmonic mean of the two. Use it with imbalanced classes, where accuracy can mislead.

Moving the threshold trades one for the other. From our breast-cancer run (positive = malignant):

| Threshold | Precision | Recall | F1 |
|---|---|---|---|
| 0.20 | 0.719 | 1.000 | 0.837 |
| 0.50 | 0.954 | 0.969 | 0.961 |
| 0.80 | 1.000 | 0.672 | 0.804 |

### Overfitting vs underfitting
| | Underfitting (high bias) | Good fit | Overfitting (high variance) |
|---|---|---|---|
| Train score | Low | High | Very high |
| Validation score | Low | High | Much lower than train |
| Fix | Bigger model, more features, train longer | – | More data, Dropout, L2, EarlyStopping, simpler model, augmentation |

Our results: polynomial degree 1 / 4 / 15 give test MSE 0.19 / **0.013** / 0.023. An unlimited decision tree scores train 1.00 vs validation 0.79 (overfit). A depth-2 tree scores 0.32 vs 0.31 (underfit). With 40 training samples, an unregularised 3×256 Keras net drives train BCE to 0.0000 while validation BCE climbs from 0.137 (epoch 3) to 0.226. Adding Dropout + L2 + EarlyStopping stops at epoch 24 and keeps the best model.

### Learning rate and batch size
- **Learning rate:** too small crawls, too large bounces or diverges. With SGD on digits for 15 epochs: lr 0.001 → 0.23 val accuracy, 0.1 → 0.96, 1.0 → 0.98, 5.0 → 0.10 (diverged).
- **Batch size:** smaller batches give more (noisier) updates per epoch. Full-batch training (1 update per epoch) reached only 0.49 accuracy in 15 epochs, against 0.96 with batch 32.
- Good defaults: Adam with lr = 1e-3 and batch size 32. Then tune.

### Feature scaling
| Scaler | Formula | Notes |
|---|---|---|
| StandardScaler | $(x-\mu)/\sigma$ | Default choice for neural nets |
| MinMaxScaler | $(x-\min)/(\max-\min)$ | Squashes to [0, 1] (images: divide by 255) |
| RobustScaler | $(x-\text{median})/\text{IQR}$ | Resistant to outliers |

Always `fit` the scaler on **training** data only, then `transform` train and test. On Wine, KNN went from **0.72** (unscaled) to **0.94 to 0.96** (scaled), and the Keras ANN from 0.91 to 0.94.

### Outliers
- **Detect:** Z-score (|z| > 3), the IQR rule (outside $Q1-1.5\,IQR$ … $Q3+1.5\,IQR$, the box-plot whiskers), or IsolationForest (multi-dimensional).
- **Handle:** remove (if they are errors), cap/winsorize, log-transform, or use robust models and scalers (HuberRegressor, RobustScaler).
- On our synthetic data (true slope 3.00), plain OLS was pulled to a slope of **4.89**. Removing flagged points gave 3.07, capping 3.32, Huber 3.18.
- Always ask **why** a point is an outlier before deleting it. Sometimes the outlier *is* the signal, as in fraud.

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `01_confusion_matrix_metrics.py` | Keras ANN on breast cancer; confusion matrix; accuracy/precision/recall/F1 by hand vs sklearn; threshold sweep; precision-recall curve |
| `02_overfitting_underfitting.py` | Polynomial under/good/over fit; sklearn learning curves; a Keras net overfitting on 40 samples vs Dropout + L2 + EarlyStopping |
| `03_learning_rate_batch_size.py` | Same Keras model on digits with 5 learning rates and 4 batch sizes; loss curves |
| `04_feature_scaling.py` | Wine dataset: no scaling vs StandardScaler vs MinMaxScaler for KNN, Logistic Regression and a Keras ANN |
| `05_outliers.py` | Synthetic data with injected outliers: Z-score, IQR, residual-IQR and IsolationForest detection; remove / cap / Huber handling |

## ▶️ How to Run
```bash
cd Week_6_Deep_Learning/Module_5_Model_Performance_Metrics
python 01_confusion_matrix_metrics.py        # --epochs 20
python 02_overfitting_underfitting.py        # --epochs 80  (~30 s)
python 03_learning_rate_batch_size.py        # --epochs 15  (~25 s)
python 04_feature_scaling.py                 # --epochs 30
python 05_outliers.py
```
All plots go to `outputs/`. Data: sklearn built-in datasets (breast cancer, digits, wine), plus **synthetic** seeded data in `02` (Part A) and `05`.

## 🧠 Key Takeaways
- Accuracy alone can hide problems. Look at the confusion matrix and choose precision or recall based on the cost of errors.
- The gap between training and validation performance is the main overfitting signal. Learning curves show it clearly.
- The learning rate is the most important hyper-parameter. Batch size trades gradient noise against the number of updates.
- Scale features (fit on train only). Neural nets and distance-based models depend on it.
- Outliers can distort squared-error models. Detect them, understand them, then remove, cap or use robust methods.

## 📝 Practice Exercises
1. In `01_confusion_matrix_metrics.py`, find the threshold that gives recall ≥ 0.99 with the highest possible precision.
2. Add `keras.layers.BatchNormalization()` to the overfitting network in `02` and compare the curves.
3. Replace SGD with Adam in `03_learning_rate_batch_size.py`. Which learning rates work now?
4. Add `RobustScaler` to `04_feature_scaling.py`, and add a few artificial outliers to the proline column to see which scaler copes best.
5. Apply the IQR rule column by column to the breast-cancer features and count how many rows would be removed. Would you remove them?
