#! /usr/bin/env python3
"""
environment_check.py
--------------------
Module 1 - Verify your Python / Anaconda installation.

Prints:
  * Python version, implementation and executable path
  * Whether you are inside a conda env or a virtualenv
  * Operating system information
  * Which of the key packages used in this 6-week course are installed
    (and their versions)

It never crashes when a package is missing - it just reports it.

Run:  python environment_check.py
"""

import importlib.util
from importlib import metadata
import os
import platform
import sys

# Packages used throughout the 6-week journey:  (import name, pip/conda name)
KEY_PACKAGES = [
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("matplotlib", "matplotlib"),
    ("seaborn", "seaborn"),
    ("sklearn", "scikit-learn"),
    ("scipy", "scipy"),
    ("nltk", "nltk"),
    ("cv2", "opencv-python"),
    ("tensorflow", "tensorflow"),
    ("django", "django"),
    ("mysql.connector", "mysql-connector-python"),
    ("jupyter_core", "jupyter"),
]

# Some packages ship under several distribution names (e.g. the "headless"
# OpenCV build used on servers). We try these alternatives for the version.
ALTERNATIVE_DISTS = {
    "opencv-python": ["opencv-python-headless", "opencv-contrib-python"],
}

MIN_PYTHON = (3, 10)


# ---------------------------------------------------------------
# 1. Interpreter information
# ---------------------------------------------------------------
def python_info() -> None:
    """Print information about the running Python interpreter."""
    print("=" * 60)
    print("PYTHON")
    print("=" * 60)
    print(f"Version        : {platform.python_version()}")
    print(f"Implementation : {platform.python_implementation()}")
    print(f"Executable     : {sys.executable}")
    ok = sys.version_info[:2] >= MIN_PYTHON
    status = "OK" if ok else f"please upgrade to {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+"
    print(f"Python >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]} : {status}")


# ---------------------------------------------------------------
# 2. Environment (conda / venv) information
# ---------------------------------------------------------------
def environment_info() -> None:
    """Detect whether we run inside a conda env or a virtualenv."""
    print("\n" + "=" * 60)
    print("ENVIRONMENT")
    print("=" * 60)
    conda_env = os.environ.get("CONDA_DEFAULT_ENV")
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    print(f"Conda env      : {conda_env or '-- (not in a conda env)'}")
    print(f"Virtualenv     : {'yes' if in_venv else 'no'}")
    print(f"sys.prefix     : {sys.prefix}")
    print(f"OS             : {platform.system()} {platform.release()} ({platform.machine()})")


# ---------------------------------------------------------------
# 3. Key packages
# ---------------------------------------------------------------
def package_version(import_name: str, dist_name: str) -> str | None:
    """Return the version of a package, or None when it is not installed.

    We use importlib.util.find_spec + importlib.metadata so we do NOT have to
    actually import heavy libraries such as TensorFlow (that would take ages).
    """
    try:
        if importlib.util.find_spec(import_name) is None:
            return None
    except ModuleNotFoundError:  # parent package missing (e.g. "mysql")
        return None
    for name in [dist_name, *ALTERNATIVE_DISTS.get(dist_name, [])]:
        try:
            return metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return "installed (version unknown)"


def packages_info() -> tuple[int, int]:
    """Print a table of key packages. Returns (installed, total)."""
    print("\n" + "=" * 60)
    print("KEY PACKAGES")
    print("=" * 60)
    print(f"{'package':<26}{'status':<10}version")
    print("-" * 60)
    installed = 0
    for import_name, install_name in KEY_PACKAGES:
        version = package_version(import_name, install_name)
        if version is None:
            print(f"{install_name:<26}{'MISSING':<10}-> pip install {install_name}")
        else:
            installed += 1
            print(f"{install_name:<26}{'OK':<10}{version}")
    return installed, len(KEY_PACKAGES)


def main() -> None:
    """Entry point."""
    python_info()
    environment_info()
    installed, total = packages_info()
    print("-" * 60)
    print(f"{installed}/{total} key packages installed.")
    if installed < total:
        print("Install missing ones later - each week's README lists what it needs.")


if __name__ == "__main__":
    main()
