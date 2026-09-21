# Load the cleaned CSVs into the BankChurn SQL Server database.
#
# The server is read from the environment so nothing machine-specific is
# committed. Set it once per machine:
#
#   PowerShell :  setx SQLSERVER_HOST "MYLAPTOP\SQLEXPRESS"
#   bash       :  export SQLSERVER_HOST='MYLAPTOP\SQLEXPRESS'
#
# Defaults to localhost\SQLEXPRESS, which is correct for a standard local
# SQL Server Express install.

import os
from pathlib import Path

import pandas as pd
import pyodbc

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"

SERVER = os.getenv("SQLSERVER_HOST", r"localhost\SQLEXPRESS")
DATABASE = os.getenv("SQLSERVER_DB", "BankChurn")
DRIVER = os.getenv("SQLSERVER_DRIVER", "SQL Server")

# Each table is loaded from its OWN csv. The column order here must match the
# INSERT column list below it.
TABLES = {
    "demographic": {
        "csv": "demographic.csv",
        "columns": ["CustomerId", "Gender", "Age", "Salary", "LocationId", "Churned"],
        "dtypes": {"CustomerId": int, "Age": int, "Salary": float,
                   "LocationId": int, "Churned": int},
    },
    "location": {
        "csv": "location.csv",
        "columns": ["LocationId", "Geography"],
        "dtypes": {"LocationId": int},
    },
    "account": {
        "csv": "account.csv",
        "columns": ["CustomerId", "Tenure", "Balance", "NumProducts",
                    "HasCreditCard", "IsActive"],
        "dtypes": {"CustomerId": int, "Tenure": int, "Balance": float,
                   "NumProducts": int, "HasCreditCard": int, "IsActive": int},
    },
}


def connect():
    conn = pyodbc.connect(
        f"Driver={{{DRIVER}}};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        "Trusted_Connection=yes;"
    )
    conn.autocommit = False
    return conn


def load_table(cursor, table, spec):
    """Insert one csv into one table. IDENTITY_INSERT is turned back OFF
    afterwards: SQL Server allows it on only one table at a time, so leaving
    it ON makes the next table fail."""
    path = DATA_DIR / spec["csv"]
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run the cleaning scripts first.")

    df = pd.read_csv(path)

    missing = [c for c in spec["columns"] if c not in df.columns]
    if missing:
        raise ValueError(f"{spec['csv']} is missing columns {missing} needed by {table}")

    for column, caster in spec["dtypes"].items():
        df[column] = df[column].astype(caster)

    placeholders = ", ".join("?" for _ in spec["columns"])
    column_list = ",\n            ".join(spec["columns"])
    statement = (
        f"INSERT INTO {table} (\n            {column_list}\n        )\n"
        f"        VALUES ({placeholders})"
    )

    cursor.execute(f"SET IDENTITY_INSERT {table} ON")
    try:
        cursor.fast_executemany = True
        cursor.executemany(statement, df[spec["columns"]].values.tolist())
    finally:
        cursor.execute(f"SET IDENTITY_INSERT {table} OFF")

    return len(df)


def main():
    print(f"Connecting to {SERVER} / {DATABASE}")
    conn = connect()
    cursor = conn.cursor()
    try:
        # location first: demographic.LocationId references it.
        for table in ("location", "demographic", "account"):
            rows = load_table(cursor, table, TABLES[table])
            conn.commit()
            print(f"  {table:<12} {rows:>6} rows inserted")
        print("Done.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
