# src/eda.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# 圖片儲存資料夾
OUTPUT_DIR = "C:/Users/user/PycharmProjects/PythonProject1/customer_personality_pipeline/plot"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 設定圖表風格
sns.set(style="whitegrid", palette="pastel")
plt.rcParams.update({'figure.max_open_warning': 0})

def load_data():
    df = pd.read_csv("C:/Users/user/Downloads/marketing_campaign.csv", sep="\t")
    return df

def preprocess(df):
    # 數值型欄位用中位數（median）補值
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    for col in num_cols:
        median = df[col].median()
        df[col] = df[col].fillna(median)


    # 建立新欄位
    df["Age"] = 2025 - df["Year_Birth"]
    spend_cols = [col for col in df.columns if col.startswith("Mnt")]
    df["TotalSpend"] = df[spend_cols].sum(axis=1)
    df["Children"] = df["Kidhome"] + df["Teenhome"]
    df["Customer_For"] = pd.to_datetime("2025-01-01") - pd.to_datetime(df["Dt_Customer"], dayfirst=True)
    df["Customer_For"] = df["Customer_For"].dt.days // 365

    return df

def plot_age_distribution(df):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Age'], bins=20, kde=True)
    plt.title("顧客年齡分布")
    plt.savefig(f"{OUTPUT_DIR}/age_distribution.png")
    plt.close()

def plot_income_by_education(df):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Education", y="Income", data=df)
    plt.xticks(rotation=45)
    plt.title("不同教育程度的收入分布")
    plt.savefig(f"{OUTPUT_DIR}/income_by_education.png")
    plt.close()

def plot_spending_distribution(df):
    product_cols = ['MntWines', 'MntFruits', 'MntMeatProducts',
                    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(8, 6))
    df[product_cols].mean().sort_values().plot(kind='barh')
    plt.title("各產品類別平均消費金額")
    plt.xlabel("平均金額")
    plt.savefig(f"{OUTPUT_DIR}/product_spending_bar.png")
    plt.close()

def plot_response_by_income(df):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Response', y='Income', data=df)
    plt.title("行銷響應 vs 收入")
    plt.xticks([0, 1], ['No', 'Yes'])
    plt.savefig(f"{OUTPUT_DIR}/response_by_income.png")
    plt.close()

def plot_recency_vs_spend(df):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x='Recency', y='TotalSpend', hue='Response', data=df)
    plt.title("Recency 與總消費金額")
    plt.savefig(f"{OUTPUT_DIR}/recency_vs_spend.png")
    plt.close()

def run_eda():
    df = load_data()
    df = preprocess(df)

    print("🔍 執行資料探索與圖表儲存中...")
    plot_age_distribution(df)
    plot_income_by_education(df)
    plot_spending_distribution(df)
    plot_response_by_income(df)
    plot_recency_vs_spend(df)
    print(f"✅ 圖表已輸出至：{OUTPUT_DIR}/")

if __name__ == '__main__':
    run_eda()
