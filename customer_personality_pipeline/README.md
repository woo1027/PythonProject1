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