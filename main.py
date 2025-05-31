# from data_loader import load_data, save_data
# from text_cleaner import clean_text
# from translator import translate_to_chinese
# import time
#
#
# def main():
#     start_time = time.time()  # 記錄開始時間
#
#     df = load_data("C:/Users/user/Downloads/t.csv")
#     df['clean_text'] = df['comment_text'].map(clean_text)
#     df['translated_text'] = df['clean_text'].map(translate_to_chinese)
#     save_data(df, "C:/Users/user/PycharmProjects/PythonProject1/translated.csv")
#
#     end_time = time.time()  # 記錄結束時間
#     elapsed_time = end_time - start_time
#     print(f"處理完成，總共耗時：{elapsed_time:.2f} 秒")
#
# if __name__ == "__main__":
#     main()
#


import os
import json
import time
import torch
import torch.nn as nn
from transformers import BertTokenizer
from data_loader import load_data, save_data
from text_cleaner import clean_text
from translator import translate_to_chinese
from bert_model.dataset import prepare_dataloader_from_csv
from bert_model.model import BERTClassifier

# ===== 前處理 + 翻譯 =====
def preprocess_and_translate(raw_csv_path, output_csv_path):
    start_time = time.time()
    df = load_data(raw_csv_path)
    df['clean_text'] = df['comment_text'].map(clean_text)
    df['translated_text'] = df['clean_text'].map(translate_to_chinese)
    save_data(df, output_csv_path)
    elapsed_time = time.time() - start_time
    print(f"資料前處理與翻譯完成，耗時：{elapsed_time:.2f} 秒")


# ===== 模型訓練流程 =====
def train_model_pipeline(csv_path, text_column, label_columns, model_dir, num_epochs=10):
    start_time1 = time.time()
    # 1. 設定模型與訓練參數
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BERTClassifier(model_name='bert-base-chinese', num_labels=len(label_columns)).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    loss_fn = nn.BCEWithLogitsLoss()

    # 2. 準備資料
    train_loader, val_loader = prepare_dataloader_from_csv(
        file_path=csv_path,
        text_column=text_column,
        label_columns=label_columns,
        tokenizer_name='bert-base-chinese',
        batch_size=16,
        max_length=128,
        val_size=0.2
    )

    # 3. 開始訓練
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        correct_predictions = 0
        total_predictions = 0

        for step, batch in enumerate(train_loader):
            input_ids, attention_mask, labels = [t.to(device) for t in batch]
            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask=attention_mask)
            loss = loss_fn(outputs, labels)
            total_loss += loss.item()
            loss.backward()
            optimizer.step()

            predictions = torch.round(torch.sigmoid(outputs))
            correct_predictions += (predictions == labels).sum().item()
            total_predictions += labels.size(0) * labels.size(1)

        train_accuracy = correct_predictions / total_predictions
        print(f'[Epoch {epoch+1}] Train Loss: {total_loss/len(train_loader):.4f}, Accuracy: {train_accuracy:.4f}')

        # 驗證
        model.eval()
        val_loss = 0
        correct_predictions = 0
        total_predictions = 0

        with torch.no_grad():
            for batch in val_loader:
                input_ids, attention_mask, labels = [t.to(device) for t in batch]
                outputs = model(input_ids, attention_mask=attention_mask)
                loss = loss_fn(outputs, labels)
                val_loss += loss.item()
                predictions = torch.round(torch.sigmoid(outputs))
                correct_predictions += (predictions == labels).sum().item()
                total_predictions += labels.size(0) * labels.size(1)

        val_accuracy = correct_predictions / total_predictions
        print(f'[Epoch {epoch+1}] Val Loss: {val_loss/len(val_loader):.4f}, Val Accuracy: {val_accuracy:.4f}')
        elapsed_time1 = time.time() - start_time1
        print(f"BERT模型訓練完成，耗時：{elapsed_time1:.2f} 秒")

    # 4. 儲存模型與設定
    os.makedirs(model_dir, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(model_dir, "pytorch_model.bin"))
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    tokenizer.save_pretrained(model_dir)
    config = {"model_type": "bert", "num_labels": len(label_columns)}
    with open(os.path.join(model_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# ===== 主程式入口 =====
if __name__ == "__main__":
    raw_csv = "C:/Users/user/Downloads/train.csv"
    # raw_csv = "C:/Users/user/Downloads/t.csv"
    processed_csv = "C:/Users/user/PycharmProjects/PythonProject1/translated.csv"
    model_save_dir = "Saved_model"

    label_cols = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
    text_col = "translated_text"

    preprocess_and_translate(raw_csv, processed_csv)
    train_model_pipeline(processed_csv, text_col, label_cols, model_save_dir, num_epochs=10)