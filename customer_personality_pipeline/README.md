# 🧠 顧客分析與資料探勘

本專案目標 理解顧客屬性與行為、分析與預測顧客的「健康狀況」
呈現，顧客的參與度、價值貢獻、忠誠度（RFM/CLV/Segmentation），並提供視覺化分析與洞見
針對行銷與產品策略提供建議。
## 📁 資料摘要
| 欄位名稱                                            | 說明               |
| ----------------------------------------------- | ---------------- |
| `ID`                                            | 客戶編號             |
| `Year_Birth`                                    | 出生年份             |
| `Education`                                     | 教育程度             |
| `Marital_Status`                                | 婚姻狀況             |
| `Income`                                        | 年收入              |
| `Kidhome`, `Teenhome`                           | 分別代表家庭中小孩與青少年的數量 |
| `Dt_Customer`                                   | 成為顧客的日期          |
| `Recency`                                       | 最近一次購買距今的天數      |
| `MntWines`, `MntFruits`, `MntMeatProducts`, ... | 各類產品花費金額         |
| `NumDealsPurchases`                             | 促銷購買次數           |
| `NumWebPurchases`, `NumCatalogPurchases`, ...   | 不同通路購買次數         |
| `Complain`                                      | 是否曾抱怨            |
| `Response`                                      | 是否對行銷活動有反應（1 為有） |

## 🔍 延伸分析

1. 🧓 年齡 (Age)

![image](age_distribution.png)
- Age ⬇️ vs TotalSpend ⬇️（中度負相關）

  年輕人總消費金額較高，顯示潛力族群為年輕族群。 

- Age ⬇️ vs Children ⬇️（中強負相關）

  年輕者更可能有小孩，影響產品偏好（如食物、日常用品）

- Age ⬇️ vs Response ⬆️（可能微弱正向）

  年輕族群對行銷活動回應度更高，可針對此族群推行促銷。

2. 💰 收入 (Income)
- Income ⬆️ vs TotalSpend ⬆️（高度正相關）

    明確呈現收入越高者，總消費越高，是潛在「高價值客戶」。

- Income ⬆️ vs MntWines, MntGoldProds ⬆️（中度正相關）

    高價產品有高收入偏好傾向，建議針對此族群做精緻化推薦。

- Income vs Response: 幾乎無相關或輕微負相關

    高收入者不一定對行銷活動有興趣，需搭配其他特徵細分。

3. 📦 各消費產品金額（MntXXX）
- MntWines、MntGoldProds、MntMeatProducts 間彼此相關性高（> 0.7）

    表示消費者若傾向購買某類產品，往往也在其他類別有消費。

    建議進行：顧客分群（Clustering） 或 主成分分析（PCA）。

- TotalSpend ⬆️ vs 所有 MntXXX 欄位 ⬆️（高度正相關）

    可將 TotalSpend 作為消費潛力指標。

4. 📅 Recency 與時間/忠誠度變數
- Recency ⬆️ vs TotalSpend ⬇️（中度負相關）

    越久未消費者，過去總支出也較少，應針對其設計「喚醒活動」。

- Customer_For ⬆️ vs Response ⬆️（微弱正相關）

    顧客關係越久可能對品牌有較高忠誠度，值得觀察其回應情形。
5. 👨‍👩‍👧‍👦 家庭結構
- Children ⬆️ vs MntMeatProducts, MntFruits ⬆️（中度正相關）

    有小孩者更傾向購買家庭型食品，可導入家庭促銷方案。

- Children vs Response ⬇️（可能負相關）

    育兒壓力者較難參與活動，需考慮「便利性導向行銷」。

## 📁 專案架構
```js
customer-personality-pipeline/
│
├── data/                    # 存放原始資料與處理後資料（勿上傳大檔案）
│   ├── raw/
│   └── processed/
│
├── notebooks/               # Jupyter EDA 與實驗筆記本
│   └── eda.ipynb
│
├── src/                     # Python 模組：ETL、模型、訓練、預測等
│   ├── data_loader.py
│   ├── preprocessing.py    
│   ├── model.py
│   ├── train.py
│   └── predict.py
│
├── outputs/                 # 輸出報表與模型（e.g., .pkl）
│   ├── models/
│   └── metrics/
│
├── .github/                 # GitHub Actions 設定
│   └── workflows/
│       └── ci-cd.yml
│
├── requirements.txt         # 環境依賴
├── Dockerfile               # 建立容器化模型部署
├── app.py                   # FastAPI 或 Flask 應用程式
├── README.md
└── .gitignore

```

## 成果
===== Top 3 Models by Cross-Validation Accuracy =====
1. catboost - Accuracy: 0.8592 ± 0.0128
2. naive_bayes - Accuracy: 0.8538 ± 0.0163
3. random_forest - Accuracy: 0.8511 ± 0.0165