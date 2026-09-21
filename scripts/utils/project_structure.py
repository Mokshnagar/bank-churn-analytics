from pathlib import Path

folders = [
    "documentation/docs",
    "documentation/figures",

    "data/raw",
    "data/processed",

    "scripts/data_cleaning",
    "scripts/data_ingestion",

    "eda_queries",

    "notebook/statistical_testing",

    "predictive_modelling/building",
    "predictive_modelling/responsible_ai",

    "data_visualization"
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)
