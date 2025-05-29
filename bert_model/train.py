import os
import json
import torch
import torch.nn as nn
from transformers import BertTokenizer
from bert_model.dataset import prepare_dataloader_from_csv
from bert_model.model import BERTClassifier

# ===== 1. 設定參數與設備 =====
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BERTClassifier(model_name='bert-base-chinese', num_labels=6).to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
loss_fn = nn.BCEWithLogitsLoss()

# ===== 2. 載入資料 =====
csv_path = "C:/Users/user/PycharmProjects/PythonProject1/translated.csv"
text_column = "translated_text"
label_columns = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

train_loader, val_loader = prepare_dataloader_from_csv(
    file_path=csv_path,
    text_column=text_column,
    label_columns=label_columns,
    tokenizer_name='bert-base-chinese',
    batch_size=16,
    max_length=128,
    val_size=0.2
)


# 訓練紀錄用
train_loss_history = []
train_acc_history = []
val_loss_history = []
val_accuracy_history = []

# 訓練函數
def train_model(model, train_loader, val_loader, optimizer, device, num_epochs):
    model = model.to(device)
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        correct_predictions = 0
        total_predictions = 0

        for step, batch in enumerate(train_loader):
            input_ids, attention_mask, labels = [t.to(device) for t in batch]

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask=attention_mask)
            loss_fn = torch.nn.BCEWithLogitsLoss()
            loss = loss_fn(outputs, labels)
            total_loss += loss.item()

            loss.backward()
            optimizer.step()

            # 紀錄準確率
            train_loss_history.append(loss.item())
            predictions = torch.round(torch.sigmoid(outputs))
            correct_predictions += (predictions == labels).sum().item()
            total_predictions += labels.size(0) * labels.size(1)

            if (step + 1) % 100 == 0:
                print(f'Epoch {epoch+1}, Step {step+1}, Training Loss: {loss.item():.4f}')

        train_accuracy = correct_predictions / total_predictions
        train_acc_history.append(train_accuracy)

        # 驗證階段
        model.eval()
        val_loss = 0
        correct_predictions = 0
        total_predictions = 0

        with torch.no_grad():
            for batch in val_loader:
                input_ids, attention_mask, labels = [t.to(device) for t in batch]
                outputs = model(input_ids, attention_mask=attention_mask)
                loss_fn = torch.nn.BCEWithLogitsLoss()
                loss = loss_fn(outputs, labels)
                val_loss += loss.item()

                predictions = torch.round(torch.sigmoid(outputs))
                correct_predictions += (predictions == labels).sum().item()
                total_predictions += labels.size(0) * labels.size(1)

        val_accuracy = correct_predictions / total_predictions
        val_loss_history.append(val_loss / len(val_loader))
        val_accuracy_history.append(val_accuracy)

        print(f'Epoch {epoch+1}: Train Loss: {total_loss/len(train_loader):.4f}, Train Acc: {train_accuracy:.4f}, Val Loss: {val_loss/len(val_loader):.4f}, Val Acc: {val_accuracy:.4f}')

# 開始訓練
train_model(model, train_loader, val_loader, optimizer, device, num_epochs=10)


# 建立資料夾（若不存在）
os.makedirs("Saved_model", exist_ok=True)

# 儲存模型權重
torch.save(model.state_dict(), "Saved_model/pytorch_model.bin")

# 儲存 tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
tokenizer.save_pretrained("Saved_model")

# 儲存 config.json
config = {
    "model_type": "bert",
    "num_labels": 6
}
with open("Saved_model/config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
