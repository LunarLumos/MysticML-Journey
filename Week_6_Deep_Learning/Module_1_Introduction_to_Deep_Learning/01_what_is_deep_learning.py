"""
Module 1 - Introduction to Deep Learning
=========================================
A printable "cheat sheet" + one conceptual plot:

  1. What Deep Learning is (AI > ML > DL)
  2. Deep Learning vs Machine Learning (comparison table)
  3. Different Deep Learning techniques (ANN, CNN, RNN/LSTM, ...)
  4. A plot of the classic "performance vs amount of data" intuition

No TensorFlow needed for this script - just plain Python + matplotlib.

Run:
    python 01_what_is_deep_learning.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


# ---------------------------------------------------------------------------
# Helper: print a simple text table
# ---------------------------------------------------------------------------
def print_table(headers, rows):
    """Print a list of rows as a neatly aligned text table."""
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    print(line)
    print("| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |")
    print(line)
    for row in rows:
        print("| " + " | ".join(str(c).ljust(w) for c, w in zip(row, widths)) + " |")
    print(line)


# ---------------------------------------------------------------------------
# 1. What is Deep Learning?
# ---------------------------------------------------------------------------
def intro():
    """Explain where Deep Learning sits inside AI and ML."""
    print("=" * 70)
    print("1. WHAT IS DEEP LEARNING?")
    print("=" * 70)
    print(
        "Artificial Intelligence  -> any technique that makes machines act 'smart'\n"
        "  Machine Learning       -> machines LEARN patterns from data\n"
        "    Deep Learning        -> ML using neural networks with MANY layers\n"
    )
    print(
        "A deep neural network stacks layers of simple units ('neurons').\n"
        "Early layers learn simple features (edges, short patterns), deeper\n"
        "layers combine them into complex features (faces, words, meaning).\n"
        "The key idea: the network learns the FEATURES itself - you don't\n"
        "hand-engineer them like in classic ML.\n"
    )


# ---------------------------------------------------------------------------
# 2. Deep Learning vs Machine Learning
# ---------------------------------------------------------------------------
def dl_vs_ml():
    """Print a comparison table between classic ML and Deep Learning."""
    print("=" * 70)
    print("2. DEEP LEARNING vs MACHINE LEARNING")
    print("=" * 70)
    headers = ["Aspect", "Machine Learning", "Deep Learning"]
    rows = [
        ["Data needed", "Works with small/medium data", "Shines with LARGE data"],
        ["Features", "Hand-crafted by humans", "Learned automatically"],
        ["Hardware", "CPU is fine", "GPU/TPU helps a lot"],
        ["Training time", "Seconds - minutes", "Minutes - days"],
        ["Interpretability", "Often easy (trees, coefs)", "Hard ('black box')"],
        ["Best for", "Tabular / structured data", "Images, audio, text, video"],
        ["Examples", "LinearReg, KNN, RandomForest", "ANN, CNN, RNN, LSTM, Transformer"],
    ]
    print_table(headers, rows)
    print()


# ---------------------------------------------------------------------------
# 3. Different Deep Learning techniques
# ---------------------------------------------------------------------------
def techniques():
    """Print an overview of the main deep learning architectures."""
    print("=" * 70)
    print("3. DIFFERENT DEEP LEARNING TECHNIQUES")
    print("=" * 70)
    headers = ["Technique", "Good at", "Example use", "This course"]
    rows = [
        ["ANN / MLP (dense layers)", "Tabular data", "Churn, price prediction", "Module 2"],
        ["CNN (convolutional)", "Images / grids", "Digit & face recognition", "Module 3"],
        ["RNN / LSTM / GRU", "Sequences / time", "Stock prices, text", "Module 4"],
        ["Autoencoder", "Compression, anomalies", "Fraud detection", "-"],
        ["GAN", "Generating data", "Fake faces, art", "-"],
        ["Transformer", "Long sequences, language", "ChatGPT, translation", "-"],
        ["Deep Reinforcement Learning", "Decision making", "Game-playing agents", "-"],
    ]
    print_table(headers, rows)
    print()


# ---------------------------------------------------------------------------
# 4. Conceptual plot: performance vs amount of data
# ---------------------------------------------------------------------------
def plot_performance_vs_data():
    """Draw the (illustrative, not measured!) 'more data helps DL' curve."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    data = np.linspace(0, 10, 200)
    classic_ml = 0.70 * (1 - np.exp(-1.2 * data))           # plateaus early
    small_nn = 0.80 * (1 - np.exp(-0.6 * data))
    deep_nn = 0.97 / (1 + np.exp(-(data - 5)))               # keeps growing

    plt.figure(figsize=(7, 4.5))
    plt.plot(data, classic_ml, label="Classic ML")
    plt.plot(data, small_nn, label="Small neural network")
    plt.plot(data, deep_nn, label="Deep neural network")
    plt.xlabel("Amount of training data  →")
    plt.ylabel("Performance  →")
    plt.title("Why Deep Learning took off (illustrative curve)")
    plt.xticks([])
    plt.yticks([])
    plt.legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "performance_vs_data.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"Saved conceptual plot -> {out}")


if __name__ == "__main__":
    intro()
    dl_vs_ml()
    techniques()
    plot_performance_vs_data()
