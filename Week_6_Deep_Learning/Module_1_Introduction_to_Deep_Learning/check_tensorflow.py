"""
check_tensorflow.py - verify your TensorFlow / Keras installation
==================================================================
Run this right after installing TensorFlow. It prints:
  * Python, TensorFlow and Keras versions
  * the devices TensorFlow can see (CPU, GPU / Apple "Metal" GPU)
  * a tiny matrix multiplication to prove TF actually works

Run:
    python check_tensorflow.py
"""

import os
import platform
import sys

# Hide TensorFlow's very chatty C++ start-up logs (0 = all, 3 = errors only)
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")


def main():
    """Import TensorFlow and print a short health report."""
    print("=" * 60)
    print("TensorFlow installation check")
    print("=" * 60)
    print(f"Python      : {sys.version.split()[0]}")
    print(f"Platform    : {platform.system()} {platform.machine()}")

    try:
        import tensorflow as tf
    except ImportError:
        print("\n[X] TensorFlow is NOT installed.")
        print("    Install it with:  pip install tensorflow")
        print("    (Apple Silicon: optionally also  pip install tensorflow-metal)")
        sys.exit(1)

    from tensorflow import keras

    print(f"TensorFlow  : {tf.__version__}")
    print(f"Keras       : {keras.__version__}")

    # ---- Devices ----------------------------------------------------------
    cpus = tf.config.list_physical_devices("CPU")
    gpus = tf.config.list_physical_devices("GPU")
    print(f"CPUs found  : {len(cpus)}")
    print(f"GPUs found  : {len(gpus)}  {[g.name for g in gpus]}")
    if not gpus:
        print("  -> Training will run on the CPU. That is totally fine for this course.")
        if platform.system() == "Darwin" and platform.machine() == "arm64":
            print("  -> Apple Silicon tip: `pip install tensorflow-metal` enables the GPU.")

    # ---- Tiny computation ---------------------------------------------------
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0], [1.0]])
    print("\nTest: [[1,2],[3,4]] @ [[1],[1]] =", tf.matmul(a, b).numpy().ravel().tolist())
    print("\n[OK] TensorFlow is working!")


if __name__ == "__main__":
    main()
