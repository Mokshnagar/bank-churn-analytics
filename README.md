<div align="center">
  <h1>End-to-End Banking Customer Churn Analytics &amp; Predictive Modeling</h1>
  <p><strong>Moksh Nagar</strong></p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/SQL-Advanced%20Analytics-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Statistics-Hypothesis%20Testing-orange?style=flat-square"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-Churn%20Classification-success?style=flat-square"/>
  <img src="https://img.shields.io/badge/Tableau-Interactive%20Dashboard-purple?style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square"/>
</p>

---

## Business problem

Acquiring a banking customer costs considerably more than retaining one, yet most
retention effort is reactive. This project builds the full path from raw customer
records to a churn model and a decision-support dashboard, so that at-risk
customers can be identified before they leave.

**Dataset:** 10,000 customers, 2,037 of whom churned (20.4%).

---

## Headline findings

The statistical testing stage is the part of this project that changed the
conclusion, so it leads.

| Hypothesis | Test | Result | Effect size | Verdict |
|---|---|---|---|---|
| Account balance differs between churned and retained | Welch t-test | t = 1.35, **p = 0.176** | Cohen's d = 0.04 | **No effect** |
| Activity status is associated with churn | Chi-square | χ² = 242.99, **p = 8.8e-55** | Cramér's V = 0.156 | **Real association** |
| Tenure differs by country | One-way ANOVA | F = 0.92, **p = 0.470** | η² = 0.0005 | **No effect** |

**What this means:** of the three candidate drivers tested, only *account activity*
survives. Balance does not separate churners from non-churners, and tenure does not
vary meaningfully by country. Inactive customers make up 1,302 of the 2,037 churn
cases (64%) despite being a minority of the customer base.

This is a negative-result finding and it is reported as one. Two of the three
hypotheses failed, and the dashboard is built around the one that held.

---

## Model comparison

All models evaluated on the held-out test set. Churn is the positive class.
Recall is the primary metric, since the cost of missing a churner exceeds the
cost of a false alarm.

| Model | Recall | Precision | F1 | ROC AUC |
|---|---|---|---|---|
| **SVM (RBF)** | **0.711** | 0.474 | 0.569 | **0.830** |
| XGBoost | 0.666 | 0.474 | 0.554 | 0.829 |
| Random Forest | 0.636 | 0.505 | 0.563 | 0.828 |
| SVM (polynomial) | 0.671 | 0.496 | 0.570 | see note |
| Logistic Regression | 0.652 | 0.328 | 0.437 | 0.743 |

**Selected model:** SVM with RBF kernel. It recovers 71% of churners at an AUC of
0.830. The top three models are within 0.003 AUC of each other, so the choice rests
on recall, not on a meaningful ranking difference.

> **Known issue:** the polynomial SVM notebook reports ROC AUC = 0.170. A value
> below 0.5 means the predicted probability column is inverted, not that the model
> is worse than random (1 − 0.170 = 0.830, in line with the others). The
> `predict_proba` column indexing in that notebook needs fixing before its AUC
> should be quoted anywhere.

---

## Dashboard

![Dashboard](documentation/figures/Dashboard%20Mock-Up.png)

Built in Tableau (`data_visualization/Churn Prediction.twb`). Panels cover the
churn total, churn by country and continent, churn by account status, and tenure
split by churn outcome.

Design decisions worth noting:

- Red is reserved for the losing state everywhere: churned customers, and inactive
  accounts. It never means anything else.
- Country totals span only 315 to 352, an 11% range. They are shown on a
  single-hue ramp rather than six separate colours, so the near-identical values
  are not dramatised into apparent differences.
- The churn/retained pair meets a 5.4:1 contrast ratio against white.

---

## Technical approach

1. **Data modelling.** Normalised the raw extract into three tables
   (Demographic, Account, Location) with an ERD, implemented in SQL Server.
2. **Ingestion.** `scripts/data_ingestion/` creates the schema and bulk-loads the
   cleaned CSVs.
3. **Cleaning.** `scripts/data_cleaning/` handles type validation, missing values,
   categorical sanity checks, and outlier detection through shared helpers.
4. **SQL EDA.** `eda_queries/` covers churn rate across genders, average churn
   rate differences, and dynamic parameter queries.
5. **Statistical testing.** `statistical_testing/` runs the t-test, chi-square and
   ANOVA above, each with a Levene homogeneity check and a reported effect size.
6. **Modelling.** `predictive_modelling/` preprocesses, scales, and benchmarks five
   classifiers through a shared `evaluate_model` function.
7. **Dashboard.** `data_visualization/` holds the Tableau workbook.

---

## Repository structure

```
data/
  raw/                     raw_data.xlsx
  processed/               account.csv, demographic.csv, location.csv
scripts/
  data_cleaning/           per-table cleaning + shared functions
  data_ingestion/          create_tables.sql, sql_connection.py
  utils/                   environment setup, project scaffolding
eda_queries/               SQL exploratory queries
statistical_testing/       hypothesis tests with effect sizes
predictive_modelling/
  processed_data/          preprocessing.py
  experiments/             one notebook per model + evaluation_script.py
data_visualization/        Churn Prediction.twb
documentation/             ERD, data dictionary, problem definition, figures
```

---

## Setup

```bash
git clone <this-repo>
cd "End-to-End Banking Customer Churn Analytics & Predictive Modeling"

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

**SQL Server.** The connection reads its host from the environment, so nothing
machine-specific lives in the code. Set it once:

```powershell
setx SQLSERVER_HOST "YOURMACHINE\SQLEXPRESS"
```

It defaults to `localhost\SQLEXPRESS`. Optional overrides: `SQLSERVER_DB`
(default `BankChurn`) and `SQLSERVER_DRIVER` (default `SQL Server`).

Then:

```bash
sqlcmd -S "%SQLSERVER_HOST%" -i scripts/data_ingestion/create_tables.sql
python scripts/data_ingestion/sql_connection.py
```

`dataset_bundle.pkl` is not committed. Regenerate it with
`predictive_modelling/processed_data/preprocessing.py`.

---

## Limitations

- The churn dataset is a well-known public benchmark, not proprietary bank data.
  Results should not be read as generalising to a real institution.
- Precision tops out around 0.50, so roughly half of flagged customers would not
  have churned. Usable for prioritising outreach, not for automated action.
- Class imbalance (20.4% positive) is handled at the model level only. No
  resampling study was run.
- The polynomial SVM AUC bug noted above is unfixed.

---

## License

MIT. See [LICENSE](LICENSE).
