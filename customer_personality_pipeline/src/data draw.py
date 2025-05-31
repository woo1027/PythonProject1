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
def remove_outliers(df, columns):
    """
    使用 IQR 方法移除指定欄位的異常值。
    """
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df


def plot_age_distribution(df):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    sns.histplot(df['Age'], bins=20, kde=True)
    plt.title("顧客年齡分布")
    plt.savefig(f"{OUTPUT_DIR}/age_distribution.png")
    plt.close()

## 年齡分類：幼年（0–30）、壯年（31–60）、老年（61+）
    bins = [0, 31, 61, 120]
    labels = ['Youth (0–30)', 'Adult (31–60)', 'Senior (61+)']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    # 📈 平均總消費金額長條圖
    avg_spend = df.groupby('AgeGroup')['TotalSpend'].mean().reset_index()

    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    # 📈 平均總消費金額長條圖
    avg_spend = df.groupby('AgeGroup')['TotalSpend'].mean().reset_index()

def plot_total_spend_by_agegroup_life_stage(avg_spend):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=avg_spend, x='AgeGroup', y='TotalSpend', palette='Set1')
    plt.title('各年齡群的平均總消費金額')
    plt.xlabel('年齡分組')
    plt.ylabel('平均總消費金額')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/barplot_avg_spend_by_lifestage.png")
    plt.close()


def plot_response_by_agegroup(df):
# 計算每個年齡群的回應率（平均值即為Response=1的比例）
    response_rate = df.groupby("AgeGroup")["Response"].mean().reset_index()

    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=response_rate, x="AgeGroup", y="Response", palette="Set2")
    plt.title("各年齡群對行銷活動的回應率")
    plt.ylabel("平均回應率 (Response)")
    plt.xlabel("年齡群 AgeGroup")
    plt.savefig(f"{OUTPUT_DIR}/response_by_agegroup.png")
    plt.close()


def plot_channel_usage_by_agegroup(df):

    # 選擇通路欄位
    channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']

    # 計算各年齡層在各通路的平均值
    channel_means = df.groupby('AgeGroup')[channel_cols].mean().reset_index()

    # 將寬表轉換為長表以利繪圖
    df_melted = pd.melt(channel_means, id_vars='AgeGroup', var_name='Channel', value_name='AvgPurchases')

    # 繪圖
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_melted, x='Channel', y='AvgPurchases', hue='AgeGroup')
    plt.title('不同年齡層在各通路的平均購買次數')
    plt.ylabel('平均購買次數')
    plt.xlabel('購物通路')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/channel_usage_by_agegroup.png")
    plt.close()

def plot_spending_by_agegroup(df):
    # 設定產品類別欄位
    spend_cols = [
        "MntWines", "MntFruits", "MntMeatProducts",
        "MntFishProducts", "MntSweetProducts", "MntGoldProds"
    ]

    # 分組計算每個年齡群的平均消費
    agegroup_spend = df.groupby("AgeGroup")[spend_cols].mean().reset_index()

    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    agegroup_spend.set_index("AgeGroup").T.plot(kind="bar", figsize=(12, 6))
    plt.title("不同年齡群的產品類別平均消費")
    plt.ylabel("平均消費金額")
    plt.xlabel("產品類別")
    plt.xticks(rotation=20)
    plt.legend(title="AgeGroup")
    plt.savefig(f"{OUTPUT_DIR}/spending_by_agegroup.png")
    plt.close()

    return agegroup_spend

def plot_income_by_education(df):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Education", y="Income", data=df)
    plt.xticks(rotation=45)
    plt.title("不同教育程度的收入分布")
    plt.savefig(f"{OUTPUT_DIR}/income_by_education.png")
    plt.close()

def plot_income_by_spend(df):

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x="Income", y="TotalSpend", hue="AgeGroup", alpha=0.6, palette="Set2")
    sns.regplot(data=df, x="Income", y="TotalSpend", scatter=False, color="red", line_kws={"linewidth": 2})
    plt.title("收入 vs 總消費金額")
    plt.xlabel("年收入 (Income)")
    plt.ylabel("總消費金額 (TotalSpend)")
    plt.legend(title="AgeGroup")
    plt.savefig(f"{OUTPUT_DIR}/income_by_spend.png")
    plt.tight_layout()
    plt.close()

def plot_income_vs_mnt_products(df):
    """
    觀察 Income 與各 Mnt 產品類別的關係
    """
    product_cols = ['MntWines', 'MntFruits', 'MntMeatProducts',
                    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']

    plt.figure(figsize=(12, 6))
    corr_matrix = df[["Income"] + product_cols].corr()

    sns.heatmap(corr_matrix, annot=True, cmap="YlGnBu", fmt=".2f")
    plt.title("Income 與產品消費金額的相關性")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/income_vs_product_correlation.png")
    plt.close()

def plot_spending_distribution(df):
    product_cols = ['MntWines', 'MntFruits', 'MntMeatProducts',
                    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    df[product_cols].mean().sort_values().plot(kind='barh')
    plt.title("各產品類別平均消費金額")
    plt.xlabel("平均金額")
    plt.savefig(f"{OUTPUT_DIR}/product_spending_bar.png")
    plt.close()

def plot_response_by_income(df):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Response', y='Income', data=df)
    plt.title("行銷響應 vs 收入")
    plt.xticks([0, 1], ['No', 'Yes'])
    plt.savefig(f"{OUTPUT_DIR}/response_by_income.png")
    plt.close()

def plot_recency_vs_spend(df):
    matplotlib.rc('font', family='Microsoft JhengHei')
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='Recency', y='TotalSpend', hue='Response', data=df)
    plt.title("Recency 與總消費金額")
    plt.savefig(f"{OUTPUT_DIR}/recency_vs_spend.png")
    plt.close()

def run_eda():
    df = load_data()
    df = preprocess(df)  # 預處理與新欄位建立
    df = remove_outliers(df, ["Income"])

    print("🔍 執行資料探索與圖表儲存中...")
    plot_age_distribution(df)

    # 新增年齡分類欄位
    bins = [0, 31, 61, 120]
    labels = ['Youth (0–30)', 'Adult (31–60)', 'Senior (61+)']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    # 平均總消費圖（需要先 groupby 計算）
    avg_spend = df.groupby('AgeGroup')['TotalSpend'].mean().reset_index()
    # 繪圖
    plot_total_spend_by_agegroup_life_stage(avg_spend)
    plot_response_by_agegroup(df)
    plot_spending_by_agegroup(df)
    plot_income_by_education(df)
    plot_income_by_spend(df)
    plot_income_vs_mnt_products(df)
    plot_spending_distribution(df)
    plot_response_by_income(df)
    plot_recency_vs_spend(df)
    plot_income_by_education(df)
    plot_spending_distribution(df)
    plot_response_by_income(df)
    plot_recency_vs_spend(df)
    print(f"✅ 圖表已輸出至：{OUTPUT_DIR}/")

if __name__ == '__main__':
    run_eda()
