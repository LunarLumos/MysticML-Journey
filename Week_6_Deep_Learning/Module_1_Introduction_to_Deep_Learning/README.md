# Module 1 – Introduction to Deep Learning
> Week 6 · Deep Learning   |   ⬅ Previous: [Week 5](../../Week_5_Computer_Vision_and_Image_Processing)  ·  Next ➡: [Module 2 – Introduction to ANN](../Module_2_Introduction_to_ANN)

## 🎯 Learning Objectives
- Explain what Deep Learning is and where it sits inside AI and Machine Learning.
- Compare Deep Learning with classic Machine Learning and know when to use each.
- Name the main Deep Learning techniques (ANN, CNN, RNN/LSTM, and others) and what each is good at.
- Install TensorFlow and Keras (including on Apple Silicon Macs) and check that the install works.
- Build, compile, train and evaluate a first Keras model.

## ✅ Syllabus Checklist
- [x] Introduction to Deep Learning
- [x] Deep Learning vs Machine Learning
- [x] Different techniques
- [x] Installing Tensorflow | Keras

## 📖 Concepts

### What is Deep Learning?
```
Artificial Intelligence ─┐  machines that act "smart"
  Machine Learning ──────┤  learn patterns from data
    Deep Learning ───────┘  ML with neural networks that have MANY layers
```
A **deep neural network** stacks layers of simple units called **neurons**. Each layer turns what the previous layer produced into a more useful form. In an image model, early layers pick up edges, middle layers pick up shapes, and late layers pick up whole objects. The key difference from classic ML is that **the network learns the features itself**. You do not hand-craft them.

### Deep Learning vs Machine Learning
| Aspect | Machine Learning | Deep Learning |
|---|---|---|
| Data needed | Works with small/medium datasets | Shines with **large** datasets |
| Features | Hand-crafted (feature engineering) | Learned automatically |
| Hardware | CPU is fine | GPU/TPU speeds it up a lot |
| Training time | Seconds to minutes | Minutes to days |
| Interpretability | Often easy (coefficients, trees) | Hard ("black box") |
| Best for | Tabular / structured data | Images, audio, text, video |
| Examples | Linear/Logistic Regression, KNN, Random Forest | ANN, CNN, RNN, LSTM, Transformer |

> For small tabular datasets a well-tuned Random Forest or gradient-boosting model often **beats** a neural network. Deep Learning is not always the answer.

### Different Deep Learning techniques
| Technique | Good at | Example | Where in this week |
|---|---|---|---|
| **ANN / MLP** (dense layers) | Tabular data | Price prediction, churn | Module 2 |
| **CNN** (convolutional) | Images, grids | Digit/face recognition | Module 3 |
| **RNN / LSTM / GRU** | Sequences, time series | Stock prices, text | Module 4 |
| Autoencoder | Compression, anomaly detection | Fraud detection | – |
| GAN | Generating new data | Synthetic faces | – |
| Transformer | Language, long sequences | ChatGPT, translation | – |
| Deep Reinforcement Learning | Decision making | Game-playing agents | – |

### Installing TensorFlow / Keras
Keras is the high-level API that ships **inside** TensorFlow (`from tensorflow import keras`), so installing TensorFlow gives you both.

```bash
# 1. (recommended) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. install
pip install --upgrade pip
pip install tensorflow             # includes Keras 3

# 3. verify
python check_tensorflow.py
```

**Apple Silicon (M1/M2/M3/M4) notes**
- Plain `pip install tensorflow` works natively on arm64 macOS with Python 3.9 to 3.12. Use a Python from python.org or Homebrew that is **arm64**, not an x86 Python running under Rosetta. Check with `python -c "import platform; print(platform.machine())"`, which should print `arm64`.
- For GPU acceleration you can also run `pip install tensorflow-metal`. It is optional; every script in this week runs in seconds on the CPU.
- If you see `zsh: illegal hardware instruction`, you are on an x86 Python. Reinstall an arm64 Python.

**Windows / Linux**: `pip install tensorflow` (CPU). On Linux with an NVIDIA GPU, `pip install "tensorflow[and-cuda]"`. Native Windows GPU support stopped after TF 2.10, so use WSL2 for GPU training.

**Tested with:** Python 3.11, TensorFlow 2.21.0, Keras 3.15.1 (CPU, macOS arm64).

### The 5-step Keras workflow
```python
model = keras.Sequential([                     # 2. build
    keras.Input(shape=(4,)),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(3, activation="softmax"),
])
model.compile(optimizer="adam",                # 3. compile
              loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=100)        # 4. fit   (1. prepare data first!)
model.evaluate(X_test, y_test)                 # 5. evaluate / predict
```

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| `01_what_is_deep_learning.py` | Prints the AI > ML > DL explanation, the DL-vs-ML table and the techniques table; saves a conceptual "performance vs data" plot |
| `check_tensorflow.py` | Verifies the TensorFlow/Keras install: versions, CPU/GPU devices, Apple Silicon hints, a tiny `tf.matmul` |
| `02_first_keras_model.py` | First Keras models: (A) one neuron learns `y = 2x + 1`; (B) a 16-neuron network classifies Iris |

## ▶️ How to Run
```bash
cd Week_6_Deep_Learning/Module_1_Introduction_to_Deep_Learning
python check_tensorflow.py
python 01_what_is_deep_learning.py
python 02_first_keras_model.py              # default --epochs 100
python 02_first_keras_model.py --epochs 300
```
Plots are saved to `outputs/`. Sample result: the single neuron learns weight **2.000** and bias **1.000**, and the Iris network reaches about **0.97** test accuracy.

## 🧠 Key Takeaways
- Deep Learning is Machine Learning with many-layered neural networks that **learn their own features**.
- It needs more data and compute, and pays off most on unstructured data (images, audio, text).
- Each architecture fits a data type: dense layers for tables, CNNs for images, RNNs/LSTMs for sequences.
- Every Keras project follows the same steps: **prepare, build, compile, fit, evaluate**.

## 📝 Practice Exercises
1. Change Part A of `02_first_keras_model.py` to learn `y = -3x + 7`. How many epochs does it need?
2. Remove the `StandardScaler` from the Iris model. What happens to accuracy after 20 epochs?
3. Add a second hidden layer (`Dense(8, activation="relu")`) to the Iris model and compare `model.summary()` parameter counts.
4. Make a table like the DL-vs-ML one for three problems you care about, and decide whether each should use classic ML or DL.
5. (Apple Silicon) Install `tensorflow-metal` and re-run `check_tensorflow.py`. Does a GPU show up?
