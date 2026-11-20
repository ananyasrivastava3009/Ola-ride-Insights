import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("===== OLA RIDE INSIGHTS =====")

# 1. Load Dataset
file_path = "dataset/OLA_DataSet.xlsx"
df = pd.read_excel(file_path)

print("\nDataset Loaded Successfully!")
print("Original Shape:", df.shape)

# 2. Clean Column Names
df.columns = df.columns.str.strip()

# 3. Replace blank spaces with missing values
df = df.replace(r"^\s*$", np.nan, regex=True)

# 4. Check Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# 5. Remove Duplicate Rows
duplicates = df.duplicated().sum()
print("\nDuplicate Rows Found:", duplicates)

df = df.drop_duplicates()

# 6. Dataset Information
print("\nCleaned Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

# 7. Create Output Folders
os.makedirs("outputs/graphs", exist_ok=True)

# 8. Save Cleaned Dataset
df.to_csv("outputs/ola_cleaned.csv",
          index=False, encoding="utf-8-sig")

df.to_excel("outputs/ola_cleaned.xlsx",
            index=False)

# 9. Save Missing Values Report
missing = df.isnull().sum().reset_index()
missing.columns = ["Column", "Missing_Count"]
missing.to_csv("outputs/missing_values_report.csv",
               index=False)

# 10. EDA - Numeric Columns
numeric_cols = df.select_dtypes(include="number").columns

for col in numeric_cols[:6]:
    plt.figure(figsize=(7, 4))
    sns.histplot(df[col].dropna(), kde=True)
    plt.title(f"Distribution of {col}")
    plt.tight_layout()
    plt.savefig(f"outputs/graphs/{col}_distribution.png")
    plt.close()

# 11. EDA - Categorical Columns
cat_cols = df.select_dtypes(
    include=["object", "category"]
).columns

for col in cat_cols[:5]:
    if df[col].nunique() <= 30:
        plt.figure(figsize=(8, 4))
        df[col].value_counts().head(10).plot(kind="bar")
        plt.title(f"Count of {col}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"outputs/graphs/{col}_count.png")
        plt.close()

# 12. Final Summary
print("\n===== FINAL SUMMARY =====")
print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))
print("Duplicates Removed:", duplicates)
print("Remaining Missing Values:", df.isnull().sum().sum())

print("\nCleaned Dataset Saved Successfully!")
print("Graphs Saved in outputs/graphs/")