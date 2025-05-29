import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import BertConfig

# ====== 1. 設定設備與載入模型、Tokenizer ======
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "C:/Users/user/PycharmProjects/PythonProject1/bert_model/Saved_model"


# 明確指定中文 BERT 的設定
config = BertConfig.from_pretrained("bert-base-chinese", num_labels=6)
model = BertForSequenceClassification(config)
model.load_state_dict(torch.load(f"{model_path}/pytorch_model.bin", map_location=device))
model = model.to(device)

# 載入 tokenizer（這裡建議也從原始 bert-base-chinese）
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

# 多標籤分類的標籤名稱
label_columns = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

# ====== 2. 預測函數 ======
def predict_user_input(input_text, model, tokenizer, device, threshold=0.5):
    model.eval()

    # Tokenize 單筆文字
    encoding = tokenizer(
        [input_text],
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        probs = torch.sigmoid(logits)  # 機率值

    # 判斷是否超過閾值（多標籤）
    predictions = (probs > threshold).int().squeeze().tolist()

    # 回傳 dict 格式結果
    result = {label: bool(pred) for label, pred in zip(label_columns, predictions)}
    return result

# ====== 3. 測試用例 ======
if __name__ == "__main__":
    input_text = input("請輸入一段中文評論進行預測：\n> ")
    prediction = predict_user_input(input_text, model, tokenizer, device)

    print("\n📊 預測結果：")
    for label, present in prediction.items():
        print(f"- {label}: {'✅ 是' if present else '❌ 否'}")
