"""
02_logistic_parameter_significance.py
=====================================
Week 4 · Module 3 – Model Specification & Model Parameter Significance Evaluation

Which inputs REALLY matter? For logistic regression we use the Wald test:

    z_j = β̂_j / SE(β̂_j)        p-value = 2 · (1 − Φ(|z_j|))

where the standard errors come from the inverse of the Fisher information
matrix:   Cov(β̂) = (Xᵀ W X)⁻¹ ,  W = diag(p̂ (1 − p̂)).

We compute this MANUALLY (NumPy + SciPy) and, if statsmodels is installed,
print statsmodels' Logit summary to confirm. We also run a likelihood-ratio
test comparing a small vs. a large model specification.

Dataset: a SYNTHETIC "student admission" dataset generated below, where
`gre` and `gpa` truly matter and `shoe_size` is pure noise (so we know the answer!).

Run:
    python 02_logistic_parameter_significance.py
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression


def make_admissions(n: int = 400, seed: int = 1) -> pd.DataFrame:
    """Synthetic admissions data with 2 real predictors and 1 useless one."""
    rng = np.random.default_rng(seed)
    gre = rng.normal(0, 1, n)          # standardised GRE score
    gpa = rng.normal(0, 1, n)          # standardised GPA
    shoe_size = rng.normal(0, 1, n)    # irrelevant!
    logit = -0.5 + 1.2 * gre + 0.8 * gpa
    admitted = rng.random(n) < 1 / (1 + np.exp(-logit))
    return pd.DataFrame({"gre": gre, "gpa": gpa, "shoe_size": shoe_size,
                         "admitted": admitted.astype(int)})


def fit_unpenalised(X: pd.DataFrame, y: pd.Series) -> LogisticRegression:
    """Plain (un-regularised) maximum-likelihood logistic regression.

    scikit-learn >= 1.8 spells "no penalty" as C=np.inf; older versions use
    penalty=None – we support both.
    """
    try:
        return LogisticRegression(C=np.inf, max_iter=1000).fit(X, y)
    except ValueError:
        return LogisticRegression(penalty=None, max_iter=1000).fit(X, y)


def wald_table(X: pd.DataFrame, y: pd.Series) -> tuple[pd.DataFrame, float]:
    """Fit an (unpenalised) logistic regression and build a significance table."""
    # C=inf means "no regularisation" (plain maximum likelihood, like statsmodels)
    model = LogisticRegression(C=np.inf, max_iter=1000).fit(X, y)
    beta = np.concatenate([model.intercept_, model.coef_.ravel()])
    X_mat = np.column_stack([np.ones(len(X)), X.to_numpy()])
    p = model.predict_proba(X)[:, 1]
    W = p * (1 - p)
    cov = np.linalg.inv(X_mat.T @ (X_mat * W[:, None]))
    se = np.sqrt(np.diag(cov))
    z = beta / se
    pvals = 2 * stats.norm.sf(np.abs(z))
    table = pd.DataFrame({"coef": beta, "std err": se, "z": z, "P>|z|": pvals,
                          "odds ratio": np.exp(beta)},
                         index=["const"] + list(X.columns))
    log_lik = float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return table, log_lik


def main() -> None:
    """Show Wald tests and a likelihood-ratio test."""
    df = make_admissions()
    y = df["admitted"]
    full_cols = ["gre", "gpa", "shoe_size"]

    print("=" * 70)
    print("Full specification:  admitted ~ gre + gpa + shoe_size")
    print("=" * 70)
    table, ll_full = wald_table(df[full_cols], y)
    print(table.round(4))
    for name, row in table.drop(index="const").iterrows():
        verdict = "significant ✔" if row["P>|z|"] < 0.05 else "NOT significant ✘"
        print(f"  {name:<10} p={row['P>|z|']:.4f} → {verdict}")

    # --- Likelihood-ratio test: does dropping shoe_size hurt? ---
    _, ll_small = wald_table(df[["gre", "gpa"]], y)
    lr_stat = 2 * (ll_full - ll_small)
    lr_p = stats.chi2.sf(lr_stat, df=1)
    print("\n[*] Likelihood-ratio test (full vs. without shoe_size):")
    print(f"    LR = {lr_stat:.3f}, p = {lr_p:.3f} → "
          f"{'keep' if lr_p < 0.05 else 'drop'} shoe_size")

    # --- Optional confirmation with statsmodels ---
    try:
        import statsmodels.api as sm
        res = sm.Logit(y, sm.add_constant(df[full_cols])).fit(disp=False)
        print("\n[*] statsmodels Logit (should match the table above):")
        print(res.summary2().tables[1].round(4))
    except ImportError:
        print("\n[!] statsmodels not installed – skipping comparison.")


if __name__ == "__main__":
    main()
