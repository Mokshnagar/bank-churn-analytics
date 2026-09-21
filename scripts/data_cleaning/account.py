# import libraries & packages
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functions import categorical_sanity_check
from functions import validate_dtypes
from functions import missing_value_report
from functions import plot_distribution
from functions import plot_boxplot


# Load Data
BASE_DIR = Path(__file__).resolve().parents[2]
FILE_NAME = "raw_data.xlsx"
DATA_PATH = BASE_DIR / "data" / "raw" / FILE_NAME

SHEET_NAME = "Account"
df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)



# Categories Sanity Check
categorical_sanity_check(df, 
                         'IsActive', 
                         [0,1])

# Data Type Checking
expected_dtypes = {
    'Tenure': 'int64',
    'Balance': 'float64',
    'NumProducts': 'int64',
    'HasCreditCard': 'int64',
    'IsActive': 'int64'
}

validate_dtypes(df, 
                expected_dtypes)


# Null Values Checker
missing_value_report(df)


# Outlier Detection and Distribution
plot_distribution(df, 'Balance')
plot_boxplot(df, 'NumProducts')


# Dealing with missing values
df['Balance'] = df['Balance'].fillna(df['Balance'].mean(), inplace=True)


# Remove columns
df = df.drop(['AccountId'], axis=1)


# Export file
OUTPUT_DIR = BASE_DIR / "data" / "processed"
file_name = "account.csv"
file_path = OUTPUT_DIR / file_name
df.to_csv(file_path, index=False)