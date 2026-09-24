# Week 6 – Deep Learning 🧠
> 6 Weeks Machine Learning – Zero to Hero · ⬅ Previous: [Week 5 – Computer Vision & Image Processing](../Week_5_Computer_Vision_and_Image_Processing)  ·  Next ➡: [Projects](../Projects)

## Overview
This is the final week. We move from classic Machine Learning to **neural networks**. Every core idea is first built **from scratch in NumPy** (a neuron, backpropagation with a gradient check, convolution and pooling, an RNN cell), and then done again in a few lines of **TensorFlow/Keras**. The week ends with the tools used to judge any model: confusion matrices, precision/recall/F1, over- and underfitting, learning rate, batch size, feature scaling and outliers.

All datasets are either **sklearn built-ins** (iris, breast cancer, digits, wine, sample image) or **synthetic and seeded**, so every script runs **offline**. Default settings keep each script under about 1 minute on a laptop CPU.

## Modules
| # | Module | One-line summary |
|---|---|---|
| 1 | [Introduction to Deep Learning](Module_1_Introduction_to_Deep_Learning) | DL vs ML, DL techniques, installing TensorFlow/Keras (incl. Apple Silicon), first Keras model |
| 2 | [Introduction to ANN](Module_2_Introduction_to_ANN) | Neuron, activation functions, feed-forward + backprop from scratch on XOR (with gradient check), cost functions, Keras ANN |
| 3 | [Introduction to CNN](Module_3_Introduction_to_CNN) | Convolution, pooling and flatten by hand on a photo, then a Keras CNN on 8×8 digits (97.8% test accuracy) |
| 4 | [Introduction to RNN](Module_4_Introduction_to_RNN) | RNN cell from scratch, vanishing gradients, SimpleRNN vs LSTM on sine-wave forecasting |
| 5 | [Model Performance Metrics](Module_5_Model_Performance_Metrics) | Confusion matrix, precision/recall/F1, overfitting vs underfitting, learning rate & batch size, feature scaling, outliers |

## Prerequisites
- Python basics, functions and NumPy arrays (Weeks 1 and 3)
- Train/test split, scaling, classification vs regression (Week 4)
- Images as matrices (Week 5), which helps with CNNs
- High-school maths: derivatives and the chain rule (we explain as we go)

## Setup
```bash
# from the repo root, inside your virtual environment
pip install numpy matplotlib scikit-learn tensorflow
# Apple Silicon (optional GPU):  pip install tensorflow-metal

python Week_6_Deep_Learning/Module_1_Introduction_to_Deep_Learning/check_tensorflow.py
```
Tested with Python 3.11, TensorFlow 2.21.0 and Keras 3.15.1 on macOS arm64 (CPU). Every training script accepts `--epochs` so you can train longer. Seeds are fixed with `keras.utils.set_random_seed(42)`. Results can still vary slightly between machines.

Run each script from inside its module folder, for example:
```bash
cd Week_6_Deep_Learning/Module_2_Introduction_to_ANN
python 03_ann_from_scratch_xor.py
```
Figures are saved to an `outputs/` folder next to each script (git-ignored).

## How this connects to what's next
Week 6 finishes the syllabus. The next step is the **[Projects](../Projects)**, where these building blocks become complete applications. MNIST Handwritten Digit Prediction uses the CNN from Module 3 at full 28×28 scale, and Google Stock Price Prediction uses the LSTM from Module 4. Carry the Module 5 checklist (confusion matrix, learning curves, scaling, outliers) into every project.
