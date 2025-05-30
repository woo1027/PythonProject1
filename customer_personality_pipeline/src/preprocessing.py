import pandas as pd
from datetime import datetime

def preprocess(df):
    df["Age"] = datetime.now().year - df["Year_Birth"]
    df["Children"] = df["Kidhome"] + df["Teenhome"]
    spend_cols = [col for col in df.columns if col.startswith("Mnt")]
    df["TotalSpend"] = df[spend_cols].sum(axis=1)
    df["Customer_For"] = pd.to_datetime("2025-01-01") - pd.to_datetime(df["Dt_Customer"], dayfirst=True)
    df["Customer_For"] = df["Customer_For"].dt.days // 365
    return df