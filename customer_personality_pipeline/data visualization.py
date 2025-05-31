
'''
🔹 資料視覺化洞察（Matplotlib / Seaborn）
- 年齡 vs 總消費額（Total Spend）

- 婚姻狀況與消費偏好

- 收入 vs 行銷回應機率

- 不同教育層級的產品消費分佈'''


import pandas as pd


# 年齡 vs 總消費額（Total Spend）
df = pd.read_csv("C:/Users/user/PycharmProjects/PythonProject1/customer_personality_pipeline/marketing_campaign.csv",
                 sep="\t")
