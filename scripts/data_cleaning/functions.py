# Function: Categories Sanity Check
def categorical_sanity_check(df, column, valid_values):
    invalid = df[~df[column].isin(valid_values)]
    return invalid[column].value_counts()



# Function: Data Type Checking
def validate_dtypes(df, expected_dtypes: dict):
    mismatches = {}
    for col, dtype in expected_dtypes.items():
        if col in df.columns and df[col].dtype != dtype:
            mismatches[col] = (df[col].dtype, dtype)
    return mismatches






# Function: Null Values Checker
def missing_value_report(df):
    return (
        df.isnull()
          .sum()
          .to_frame("missing_count")
          .assign(missing_pct=lambda x: x.missing_count / len(df))
          .query("missing_count > 0")
    )






# Function: Outlier Detection and Distribution
import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(df, col):
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.show()

def plot_boxplot(df, col):
    sns.boxplot(x=df[col])
    plt.title(f"Outliers in {col}")
    plt.show()