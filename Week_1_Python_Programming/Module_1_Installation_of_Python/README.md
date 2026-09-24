# Module 1 – Installation of Python on Anaconda Platform
> Week 1 · Python Programming   |   ⬅ Previous: [Week 1 overview](../README.md)  ·  Next ➡: [Module 2 – Data Types and Variables](../Module_2_Data_Types_and_Variables)

## 🎯 Learning Objectives
- Install Python through the **Anaconda** distribution on Windows, macOS or Linux.
- Create and manage isolated **conda environments**.
- Launch and use **Jupyter Notebook / JupyterLab** confidently (cells, kernel, shortcuts, magics).
- Know the popular Python **editors and IDEs** and pick one for this course.
- Write, run and understand a first Python program.

## ✅ Syllabus Checklist
- [x] Introduction to installation of Anaconda
- [x] Introduction to Python Editors & IDE's (Anaconda, Jupyter etc...)
- [x] Understand Jupyter notebook
- [x] Overview of Python – Starting with Python
- [x] Exploring different IDE for Python

## 📖 Concepts

### 1. What is Anaconda?
**Anaconda** is a free Python *distribution* aimed at data science. One installer gives you:

| Component | What it is |
|---|---|
| Python interpreter | the program that runs `.py` files |
| `conda` | package **and** environment manager (installs Python libs *and* non-Python deps such as MKL, CUDA) |
| ~250 preinstalled packages | NumPy, pandas, Matplotlib, scikit-learn, Jupyter, Spyder… |
| Anaconda Navigator | a GUI launcher for Jupyter, Spyder, VS Code, and environments |

> Prefer something smaller? **Miniconda** / **Miniforge** ship only Python + conda; you install what you need.

### 2. Installing Anaconda

**Windows**
1. Download the *64-bit Graphical Installer* from <https://www.anaconda.com/download>.
2. Run the `.exe` → *Just Me* → keep the default path (avoid paths with spaces).
3. Leave "Add Anaconda to PATH" **unchecked** (recommended); use the **Anaconda Prompt** from the Start menu instead.
4. Verify in *Anaconda Prompt*: `conda --version` and `python --version`.

**macOS**
1. Download the installer for your chip (*Apple Silicon* = arm64, *Intel* = x86_64).
2. Double-click the `.pkg` and follow the wizard (or use the command-line installer: `bash Anaconda3-*-MacOSX-*.sh`).
3. Open a **new** Terminal – the prompt should begin with `(base)`.
4. Verify: `conda --version && python --version`.

**Linux**
```bash
# download the latest installer (check the website for the current file name)
wget https://repo.anaconda.com/archive/Anaconda3-<version>-Linux-x86_64.sh
bash Anaconda3-<version>-Linux-x86_64.sh     # accept licence, keep default location
source ~/.bashrc                              # or open a new terminal
conda --version && python --version
```
Say **yes** when asked to run `conda init` so conda is available in every new shell.
Don't want `(base)` auto-activated? → `conda config --set auto_activate_base false`.

### 3. Conda environments
An **environment** is an isolated folder with its own Python version and packages, so projects don't break each other.

```bash
conda create -n mysticml python=3.11      # create
conda activate mysticml                   # enter it   (prompt shows (mysticml))
conda install numpy pandas matplotlib seaborn scikit-learn jupyter   # add packages
pip install django mysql-connector-python # pip also works inside a conda env
conda env list                            # list all environments
conda list                                # packages in the active env
conda env export > environment.yml        # share / reproduce the env
conda env create -f environment.yml       # recreate it elsewhere
conda deactivate                          # leave the env
conda remove -n mysticml --all            # delete the env
```
> Rule of thumb: install with `conda` first; fall back to `pip` for packages conda doesn't have. Never `pip install` into `base`.

### 4. Jupyter Notebook
Start it from an activated env: `jupyter notebook` (classic) or `jupyter lab` (modern UI). It opens in your browser at `http://localhost:8888`.

- A **notebook** (`.ipynb`) is a JSON file of **cells**: *Code* cells and *Markdown* cells.
- A **kernel** is the Python process behind the notebook. Variables live in the kernel, so **execution order matters** (the `In [n]` counter) – use *Kernel → Restart & Run All* to check that your notebook works top-to-bottom.
- The value of the **last expression** in a cell is displayed automatically.
- **Magic commands**: `%timeit expr`, `%who`, `%pwd`, `%matplotlib inline`, `%%time` (whole cell), `!pip list` (shell command).
- Help: `len?`, `help(len)`, **Shift+Tab** for a signature, **Tab** to autocomplete.

**Essential shortcuts**

| Mode | Shortcut | Action |
|---|---|---|
| any | `Shift + Enter` | run cell, select next |
| any | `Ctrl + Enter` | run cell, stay |
| any | `Alt + Enter` | run cell, insert below |
| command (`Esc`) | `A` / `B` | insert cell above / below |
| command | `D, D` | delete cell |
| command | `Z` | undo cell deletion |
| command | `M` / `Y` | to Markdown / to Code |
| command | `C` / `V` / `X` | copy / paste / cut cell |
| command | `0, 0` | restart kernel |
| command | `I, I` | interrupt kernel |
| edit (`Enter`) | `Ctrl + /` | toggle comment |
| edit | `Ctrl + Shift + -` | split cell at cursor |

### 5. Python editors & IDEs compared

| Tool | Type | Best for | Pros | Cons |
|---|---|---|---|---|
| **Jupyter Notebook / Lab** | browser notebook | data exploration, teaching, plots | interactive, inline plots & Markdown | hidden state, weak for large apps |
| **Spyder** | IDE (ships with Anaconda) | scientific scripting | MATLAB-like variable explorer, IPython console | less general-purpose |
| **VS Code** | editor + extensions | everything (scripts, notebooks, Django) | free, fast, great Python & Jupyter extensions, Git | needs some setup |
| **PyCharm** (Community/Pro) | full IDE | larger projects, Django (Pro) | best refactoring, debugger, testing | heavy, Pro is paid |
| **IDLE** | basic editor | absolute beginners | ships with Python | very limited |
| **Google Colab** | cloud notebook | free GPU, no install | zero setup | needs internet, sessions expire |
| **Anaconda Navigator** | launcher GUI | managing envs without a terminal | point-and-click | slow, not an editor itself |

**Recommendation for this course:** VS Code (with the *Python* and *Jupyter* extensions) + Jupyter for exploration.

### 6. Overview of Python – starting with Python
- **High-level, interpreted, dynamically typed** – no compilation step, no type declarations: `x = 10`.
- **Indentation defines blocks** (4 spaces), not braces.
- **Batteries included** – huge standard library, plus PyPI with 500k+ packages.
- Run code three ways: interactive shell (`python`), a script (`python hello_python.py`), or a notebook.
- The `if __name__ == "__main__":` guard runs code only when a file is executed directly, not when imported.

```python
print("Hello, Python!")
a, b = 7, 2
print(a / b, a // b, a % b, a ** b)   # 3.5 3 1 49
```

## 📂 Files in this Module
| File | What it demonstrates |
|---|---|
| [`hello_python.py`](hello_python.py) | first program: print, variables, arithmetic operators, `type()`, which interpreter is running |
| [`environment_check.py`](environment_check.py) | verifies your install: Python version, conda/venv detection, OS, and which course packages are installed (no heavy imports – fast) |
| [`getting_started.ipynb`](getting_started.ipynb) | a small Jupyter notebook: code vs Markdown cells, kernel state, help, magics, shortcut table |

## ▶️ How to Run
```bash
cd Week_1_Python_Programming/Module_1_Installation_of_Python
conda activate mysticml            # or your own env
python hello_python.py
python environment_check.py
jupyter notebook getting_started.ipynb   # or: jupyter lab
```

## 🧠 Key Takeaways
- Anaconda = Python + conda + data-science packages + Jupyter in one installer.
- Use **one conda environment per project**; export it to `environment.yml` to reproduce it.
- In Jupyter, execution order matters – *Restart & Run All* before sharing.
- Pick the tool for the job: notebooks to explore, an IDE (VS Code/PyCharm) to build apps.

## 📝 Practice Exercises
1. Create a conda env called `week1` with Python 3.11, install `numpy`, and run `environment_check.py` inside it. Which packages are missing?
2. Export your env to `environment.yml`, delete the env, and recreate it from the file.
3. In `getting_started.ipynb`, add a Markdown cell with a heading, a bullet list and a formula `$a^2 + b^2 = c^2$`.
4. Use `%timeit` to compare `sum(range(10_000))` with a manual `for` loop that adds the numbers.
5. Open `hello_python.py` in two different IDEs from the table above and set a breakpoint in `quick_tour()`. Which debugger did you prefer?
