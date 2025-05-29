from flask import Flask, request, jsonify, render_template
import torch
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig


# 初始化 Flask
app = Flask(__name__)

# 設定設備與載入模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "bert_model/Saved_model"

# 載入 config, tokenizer 與模型（必須一致）
config = BertConfig.from_pretrained("bert-base-chinese", num_labels=6)
model = BertForSequenceClassification(config)
model.load_state_dict(torch.load(f"{model_path}/pytorch_model.bin", map_location=device))
model.to(device)
model.eval()

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

# 標籤名稱
label_columns = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    content = request.form.get("content")
    if not content:
        return jsonify({"error": "留言為空"}), 400

    # Tokenize
    inputs = tokenizer(
        [content],
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.sigmoid(logits)
        preds = (probs > 0.5).int().squeeze().tolist()

    return jsonify({"labels": preds})

if __name__ == "__main__":
    app.run(debug=True)
