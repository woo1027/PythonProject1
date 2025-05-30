# 🧠 中文多標籤有害留言分類系統

本專案基於 `bert-base-chinese` 模型，實作多標籤有害言論分類（toxic, obscene, threat, insult 等），結合 PyTorch 與 Flask，具備訓練、預測與網頁介面功能。

## 📁 專案結構
```
project/
├── bert_model/               # BERT 模型模組
│   ├── dataset.py            # PyTorch Dataset 資料處理模組
│   ├── model.py              # 模型架構定義（多標籤分類）
│   ├── predict.py            # 預測單筆文字的函式
│   ├── train.py              # 模型訓練流程，儲存至 Saved_model
│   └── __init__.py           # 模組初始化
│
├── Saved_model/             # 訓練完成模型儲存目錄
│   ├── pytorch_model.bin     # 訓練好的模型權重
│   ├── config.json           # 模型設定
│   └── tokenizer files       # tokenizer 的 vocab/tokenizer config 等
│
├── templates/               # 前端模板
│   └── index.html            # 留言表單頁面
│
├── app.py                   # Flask 後端 API 主程式，處理 /predict 路由
├── data_loader.py           # 載入/切分/處理原始資料，轉成 DataFrame
├── text_cleaner.py          # 中文文字的預處理模組（去除特殊符號等）
├── translator.py            # 翻譯模組（若原始資料為英文）
├── translated.csv           # 翻譯後的清理資料集（CSV 格式）
├── requirements.txt         # 專案所需的 Python 套件列表
└── main.py                  # 主控流程檔，整合所有流程（清理、轉換、訓練）
```
## ⚙️ 安裝方式

```bash
# 建議使用虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝套件
pip install -r requirements.txt
```
---
## 🚀 使用方式

### 🔹 1. 訓練模型

```bash
python main.py
```

訓練完成後，模型會儲存至 `Saved_model/`。

---

### 🔹 2. 啟動預測 API 伺服器

```bash
python app.py
```

啟動後開啟網頁：http://127.0.0.1:5000  
可輸入留言進行推論。

---

## 🧪 API 說明（POST /predict）

- URL：`/predict`
- 方法：POST
- 參數：
  - `content`: 使用者留言文字（表單欄位）
- 回傳：
```json
{
  "labels": [1, 0, 0, 0, 1, 0]  // 對應每個標籤是否為正類別
}
```

---

## 🏷️ 標籤定義（Label Columns）

```
["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
```

---

## ✨ 技術重點

- BERT 中文預訓練模型 (`bert-base-chinese`)
- PyTorch 多標籤分類 (`BCEWithLogitsLoss`)
- HuggingFace Transformers
- Flask API 部署
- 中文清洗 + 自動翻譯模組（Google Translate API）
- 前端表單頁面簡易操作

---

## 📌 Todo

- [ ] 支援上傳 CSV 批次預測
- [ ] 新增資料標註功能（Web 標註介面）
- [ ] 整合 Docker 容器化部署

---

## 📜 License

本專案僅供學術研究與個人作品展示，請勿用於商業用途。