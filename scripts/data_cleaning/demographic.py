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

SHEET_NAME = "Demographic"
df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)



# Outlier Detection and Distribution
plot_distribution(df, 'Age')
plot_boxplot(df, 'Age')


# Categories Sanity Check
categorical_sanity_check(df, 
                         'Churned', 
                         [0,1])

# Data Type Checking
expected_dtypes = {
    'Name': 'str',
    'Gender': 'str',
    'Age': 'int64',
    'Salary': 'float64',
    'LocationId': 'int64',
    'Churned': 'int64'
}

validate_dtypes(df, 
                expected_dtypes)


# Null Values Checker
missing_value_report(df)



# Remove columns
df = df.drop(['Name'], axis=1)


# Export file
OUTPUT_DIR = BASE_DIR / "data" / "processed"
file_name = "demographic.csv"
file_path = OUTPUT_DIR / file_name
df.to_csv(file_path, index=False)