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

SHEET_NAME = "Location"
df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)


# Export file
OUTPUT_DIR = BASE_DIR / "data" / "processed"
file_name = "location.csv"
file_path = OUTPUT_DIR / file_name
df.to_csv(file_path, index=False)