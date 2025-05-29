project/
├── Saved_model/
│   ├── bert_model.bin         # 訓練好的模型權重
│   ├── dataset.py             # PyTorch Dataset 資料處理模組
│   ├── model.py               # BERT 模型架構定義（多標籤分類）
│   ├── predict.py             # 單筆文字預測函式
│   ├── train.py               # 訓練流程，輸出模型至 Saved_model
│   └── __init__.py            # 模組初始化
│
├── templates/
│   └── index.html             # 網頁前端留言表單頁面
│
├── app.py                     # Flask 後端服務，處理 /predict 路由
├── data_loader.py             # 載入/切分/處理原始資料，轉成 DataFrame
├── text_cleaner.py            # 中文留言的預處理與清洗（去除符號等）
├── translator.py              # 翻譯模組（若原始資料為英文）
├── translated.csv             # 翻譯後的資料結果（CSV格式）
├── requirements.txt           # 專案所需的 Python 套件列表
└── main.py                    # 主控制腳本，整合所有流程
