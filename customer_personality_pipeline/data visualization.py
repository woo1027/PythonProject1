
'''
🔹 資料視覺化洞察（Matplotlib / Seaborn）
- 年齡 vs 總消費額（Total Spend）

- 婚姻狀況與消費偏好

- 收入 vs 行銷回應機率

- 不同教育層級的產品消費分佈'''


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

df = pd.read_csv("C:/Users/user/PycharmProjects/PythonProject1/customer_personality_pipeline/marketing_campaign.csv",
                 sep="\t")

# 查看遺失值
df.isnull()

# 缺失值補齊

# 數值型欄位用中位數（median）補值
df['Income'] = df['Income'].fillna(df['Income'].median())


# 新增欄位
df["Age"] = 2025 - df["Year_Birth"]
spend_cols = [col for col in df.columns if col.startswith("Mnt")]
df["TotalSpend"] = df[spend_cols].sum(axis=1)
df["Children"] = df["Kidhome"] + df["Teenhome"]
df["Customer_For"] = pd.to_datetime("2025-01-01") - pd.to_datetime(df["Dt_Customer"], dayfirst=True)
df["Customer_For"] = df["Customer_For"].dt.days // 365

# 選擇數值欄位

num_df = df.select_dtypes(include=["int64", "float64"])
matplotlib.rc('font', family='Microsoft JhengHei')
plt.figure(figsize=(15, 12))
sns.heatmap(num_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("數值變數相關性熱圖")
# 儲存圖像
plt.savefig("C:/Users/user/PycharmProjects/PythonProject1/customer_personality_pipeline/plot/correlation_heatmap.png", dpi=300, bbox_inches='tight')  # 可改為 .jpg 或 .pdf

plt.show()


#