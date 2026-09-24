# Module 6 – Data Visualization
> Week 3 · Data Analysis with Python   |   ⬅ Previous: [Module 5 – DataFrame Continued](../Module_5_Pandas_DataFrame_Continued)  ·  Next ➡: [Week 4 – Machine Learning](../../Week_4_Machine_Learning)

## 🎯 Learning Objectives
- Install Matplotlib and Seaborn and understand the Figure/Axes model
- Pick the right chart for a question: trend, relationship, comparison, distribution or composition
- Build line, scatter, bar, histogram, pie and box plots, and save them to files
- Detect outliers with the IQR and Z-score rules, and decide how to handle them
- Read a correlation heatmap before building ML models

## ✅ Syllabus Checklist
- [x] Introduction to Data Visualization | Installing Matplotlib and Seaborn
- [x] Line Plot, Scatter Plot, Bar Plot, Histogram, Pie Chart
- [x] Box Plot
- [x] Detecting Outliers
- [x] Heatmap

## 📖 Concepts

### Installing
```bash
pip install matplotlib seaborn scipy   # scipy is only used for stats.zscore
```

### Figure & Axes
```python
fig, ax = plt.subplots(figsize=(8, 4))   # Figure = canvas, Axes = one plot
ax.plot(x, y); ax.set_title(...); ax.set_xlabel(...); ax.legend()
fig.savefig("outputs/plot.png", dpi=120, bbox_inches="tight")
plt.close(fig)
```
Seaborn is built on Matplotlib. It takes a DataFrame plus column names (`data=df, x="col", hue="group"`) and applies better defaults.

### Choosing a chart
| Question | Chart | Matplotlib / Seaborn |
|---|---|---|
| How does it change over time? | Line | `ax.plot`, `sns.lineplot` |
| Are two numbers related? | Scatter | `ax.scatter`, `sns.scatterplot`, `sns.regplot` |
| Which category is bigger? | Bar | `ax.bar`/`barh`, `sns.barplot`, `sns.countplot` |
| What does the distribution look like? | Histogram | `ax.hist`, `sns.histplot(kde=True)` |
| What share of the whole? | Pie / donut | `ax.pie` |
| Spread, median, outliers per group? | Box / violin | `ax.boxplot`, `sns.boxplot`, `sns.violinplot` |
| How do many variables relate? | Heatmap | `sns.heatmap`, `ax.imshow` |

### Box plots and the IQR rule
$$ IQR = Q_3 - Q_1 \qquad \text{outlier if } x < Q_1 - 1.5\,IQR \ \text{ or } \ x > Q_3 + 1.5\,IQR $$
The box spans Q1 to Q3, the line inside is the median, whiskers reach the last point inside the fences, and dots are outliers.

### Z-score rule
$$ z = \frac{x - \mu}{\sigma} \qquad \text{outlier if } |z| > 3 $$
Z-scores assume roughly normal data. Extreme outliers inflate $\sigma$ and can hide other outliers, which is why the IQR rule is more **robust**. In `08_detecting_outliers.py` the IQR rule flags 7 points and the Z-score rule flags 5.

Handling outliers: **remove** them (only if they are errors), **cap** them (`clip` to the fences, also called winsorising), **replace** them (with the median), or **keep** them (if they are real and important).

### Correlation heatmap
`df.corr()` gives Pearson's $r \in [-1, 1]$. Show it with `sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, center=0)`, and mask the upper triangle to hide the duplicates. On Iris, petal length and petal width have r = 0.96.

## 📂 Files in this Module
All data is **synthetic and seeded** (generated inside each script), except `09_heatmap.py`, which uses scikit-learn's bundled **Iris** dataset (offline) and falls back to synthetic data if scikit-learn is missing. Every figure is saved to `outputs/` (git-ignored).

| File | What it demonstrates |
|---|---|
| `data_visualization.py` | The learner's original tour of line, bar, histogram, scatter, box and heatmap (opens windows with `plt.show()`) |
| `01_intro_matplotlib_seaborn.py` | Versions, anatomy of a plot, pyplot vs OO API, subplots, first seaborn plot |
| `02_line_plot.py` | Multi-line styled plot, pandas `.plot()`, seaborn lineplot with 95% CI |
| `03_scatter_plot.py` | Scatter + `polyfit` trend line, colour/size encoding, seaborn `hue`, `regplot` |
| `04_bar_plot.py` | Vertical/horizontal bars with labels, grouped & stacked bars, pandas bar, seaborn barplot/countplot |
| `05_histogram.py` | Effect of bins, overlapping densities, skewed data with mean vs median, KDE |
| `06_pie_chart.py` | Pie with explode/percentages, grouping small slices, donut, pandas pie |
| `07_box_plot.py` | 5-number summary, matplotlib notched boxplot, seaborn box + strip, violin plot |
| `08_detecting_outliers.py` | IQR & Z-score detection (incl. `scipy.stats.zscore`), visual comparison, remove/cap/replace strategies |
| `09_heatmap.py` | Correlation heatmap (full + masked), pivot-table heatmap, missing-values map, `imshow` |

## ▶️ How to Run
```bash
cd Week_3_Data_Analysis_with_Python/Module_6_Data_Visualization
python 01_intro_matplotlib_seaborn.py
python 02_line_plot.py
# … through …
python 09_heatmap.py
# PNGs appear in ./outputs/
```
On a headless machine, prefix commands with `MPLBACKEND=Agg`.

## 🧠 Key Takeaways
- Choose the chart for the question, not for how it looks.
- Always label axes, add a title, and include units.
- Box plots and the IQR rule give a robust outlier check. Z-scores work best on roughly normal data.
- Check a correlation heatmap before ML. Highly correlated features are redundant.
- Save figures with `savefig` and close them with `plt.close()` to free memory.

## 📝 Practice Exercises
1. Using `Module_2_Introduction_to_Pandas/data/employees.csv`, plot average salary per department as a sorted horizontal bar chart.
2. Draw a histogram of employee ages with 5 bins, and mark the mean and median lines.
3. Make a box plot of salary by department, then list every IQR outlier.
4. Generate 500 normal values plus 5 extreme ones, and compare how many outliers the IQR rule and the Z-score rule (|z| > 3) flag.
5. Build a correlation heatmap for `sklearn.datasets.load_wine()` and name the two most correlated features.
