# Module 2 – Introduction to Artificial Neural Networks (ANN)
> Week 6 · Deep Learning   |   ⬅ Previous: [Module 1 – Introduction to Deep Learning](../Module_1_Introduction_to_Deep_Learning)  ·  Next ➡: [Module 3 – Introduction to CNN](../Module_3_Introduction_to_CNN)

## 🎯 Learning Objectives
- Understand an artificial neuron: weighted sum, bias, activation.
- Know the common activation functions, their shapes and derivatives, and when to use each.
- Implement a **feed-forward** network and **backpropagation** from scratch in NumPy, and prove the gradients are correct with a **gradient check**.
- Know the three core cost functions (MSE, binary and categorical cross-entropy).
- Rebuild the same ideas in a few lines of Keras.

## ✅ Syllabus Checklist
- [x] Artificial Neural Networks (ANNs): Concept
- [x] Activation Functions
- [x] Feed Forward Neural Networks
- [x] Back Propagation
- [x] Cost Functions

## 📖 Concepts

### 1. The artificial neuron
$$ z = w_1x_1 + w_2x_2 + \dots + w_nx_n + b = \mathbf{w}\cdot\mathbf{x} + b, \qquad a = f(z) $$
- **Weights** $w$ set how important each input is. The **bias** $b$ shifts the threshold.
- $f$ is the **activation function**, which adds non-linearity.
- One neuron draws a **straight line** (a hyperplane) through the data. It can learn AND and OR but **not XOR**, which is why we need hidden layers. `01_neuron_concept.py` shows this.

An **ANN** stacks neurons into layers: input layer, one or more **hidden** layers, and an output layer. Every neuron in one layer connects to every neuron in the next ("dense" or "fully connected").

### 2. Activation functions
| Function | Formula | Range | Typical use |
|---|---|---|---|
| Sigmoid | $\frac{1}{1+e^{-z}}$ | (0, 1) | Binary output layer |
| Tanh | $\tanh(z)$ | (-1, 1) | Hidden layers (zero-centred), RNNs |
| ReLU | $\max(0, z)$ | [0, ∞) | **Default for hidden layers** |
| Leaky ReLU | $\max(\alpha z, z)$ | (-∞, ∞) | Avoids "dead" ReLU neurons |
| Softmax | $\frac{e^{z_k}}{\sum_j e^{z_j}}$ | (0, 1), sums to 1 | Multi-class output layer |

Without a non-linear activation, any stack of layers collapses into **one** linear layer. The sigmoid derivative is at most 0.25, so multiplying many of them together makes gradients shrink (**vanishing gradients**). That is why ReLU became the default.

### 3. Feed forward
Data flows input → hidden → output. For our 2-4-1 XOR network:
$$ Z_1 = XW_1 + b_1,\; A_1 = \tanh(Z_1),\; Z_2 = A_1W_2 + b_2,\; \hat{y} = \sigma(Z_2) $$

### 4. Backpropagation
Backpropagation applies the **chain rule** from the loss back to every weight:
$$ \frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial \hat y}\cdot\frac{\partial \hat y}{\partial Z_2}\cdot\frac{\partial Z_2}{\partial A_1}\cdot\frac{\partial A_1}{\partial Z_1}\cdot\frac{\partial Z_1}{\partial W_1} $$
For sigmoid + BCE the first two terms simplify to $\hat y - y$. Then **gradient descent** updates each weight: $W \leftarrow W - \eta \,\partial L/\partial W$.

**Gradient check.** Nudge each weight by ±ε and measure how the loss changes:
$\frac{L(\theta+\varepsilon)-L(\theta-\varepsilon)}{2\varepsilon}$. If the relative difference from our backprop gradient is below about 1e-7, the implementation is correct. Our run gives **3.0e-11**.

### 5. Cost functions
| Loss | Formula | Use with |
|---|---|---|
| MSE | $\frac1n\sum (y-\hat y)^2$ | Regression (linear output) |
| Binary cross-entropy | $-\frac1n\sum [y\log\hat y + (1-y)\log(1-\hat y)]$ | Binary classification (sigmoid) |
| Categorical cross-entropy | $-\frac1n\sum_i\sum_k y_{ik}\log\hat y_{ik}$ | Multi-class (softmax); `sparse_` version for integer labels |

Cross-entropy punishes **confident wrong answers** far harder than MSE does, which is why it is used for classification.

### 6. The same thing in Keras
```python
model = keras.Sequential([
    keras.Input(shape=(30,)),
    keras.layers.Dense(16, activation="relu"),    # feed forward
    keras.layers.Dense(8, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid"),
])
model.compile(optimizer="adam", loss="binary_crossentropy")   # cost + backprop
```

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `01_neuron_concept.py` | One neuron by hand; a single neuron learns AND/OR but fails on XOR |
| `02_activation_functions.py` | Sigmoid, tanh, ReLU, Leaky ReLU, softmax and their derivatives, plotted |
| `03_ann_from_scratch_xor.py` | **2-4-1 network in pure NumPy**: forward pass, BCE, backprop, gradient descent, **gradient check**, decision surface |
| `04_cost_functions.py` | MSE / BCE / CCE in NumPy, checked against `keras.losses`; plot of loss vs prediction |
| `05_keras_ann_breast_cancer.py` | Keras ANN on sklearn's Breast Cancer dataset, with training curves and a classification report |

## ▶️ How to Run
```bash
cd Week_6_Deep_Learning/Module_2_Introduction_to_ANN
python 01_neuron_concept.py
python 02_activation_functions.py
python 03_ann_from_scratch_xor.py            # --epochs 3000 --lr 1.0
python 04_cost_functions.py
python 05_keras_ann_breast_cancer.py         # --epochs 30
```
Sample results from our runs: XOR from scratch reaches a final loss of 0.0007 with all 4 outputs correct. The NumPy losses match Keras to 4 decimals. The Keras ANN reaches **0.956** test accuracy on breast cancer.

## 🧠 Key Takeaways
- A neuron is `activation(w·x + b)`. Stacking neurons with **non-linear** activations lets the network learn curved decision boundaries.
- Use ReLU in hidden layers, sigmoid for a binary output, softmax for multi-class.
- Training repeats forward pass → loss → backprop (chain rule) → gradient-descent update.
- Always sanity-check hand-written gradients with a numerical gradient check.
- Keras does all of this for you, and now you know what it is doing.

## 📝 Practice Exercises
1. In `03_ann_from_scratch_xor.py`, change the hidden layer from 4 to 2 neurons. Does it still solve XOR every time? Try several seeds.
2. Replace `tanh` in the hidden layer with ReLU (update the derivative too!) and re-run the gradient check.
3. Break backprop on purpose (for example, drop the `/ n` in `dZ2`) and watch the gradient check fail.
4. Add an MAE (mean absolute error) function to `04_cost_functions.py` and compare it with `keras.losses.MeanAbsoluteError`.
5. In the Keras breast-cancer model, swap every ReLU for sigmoid and compare accuracy after 30 epochs.
