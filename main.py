from data_loader import load_data, save_data
from text_cleaner import clean_text
from translator import translate_to_chinese
import time
from random import sample


def main():
    start_time = time.time()  # 記錄開始時間

    df = load_data("C:/Users/user/Downloads/train.csv")
    # df =  load_data("C:/Users/user/Downloads/train.csv").sample(500)
    df['clean_text'] = df['comment_text'].map(clean_text)

    print("開始翻譯...")
    df['translated_text'] = translate_to_chinese(df['clean_text'].tolist())

    save_data(df, "C:/Users/user/PycharmProjects/PythonProject1/translated.csv")

    end_time = time.time()  # 記錄結束時間
    elapsed_time = end_time - start_time
    print(f"處理完成，總共耗時：{elapsed_time:.2f} 秒")

if __name__ == "__main__":
    main()

#
#
# import os
# import json
# import time
# import torch
# from transformers import BertTokenizer
# from bert_model.dataset import prepare_dataloader_from_csv
# from bert_model.model import BERTClassifier
# from bert_model.train import train_model
#
# # 主程式入口
# def main():
#     start_time = time.time()  # 記錄開始時間
#
#     # df = load_data("C:/Users/user/Downloads/train.csv")
#     df =  load_data("C:/Users/user/Downloads/train.csv").sample(200)
#     df['clean_text'] = df['comment_text'].map(clean_text)
#
#     # 翻譯資料
#     df['translated_text'] = translate_to_chinese(df['clean_text'].tolist())
#
#     # 儲存翻譯後資料
#     translated_path = "C:/Users/user/PycharmProjects/PythonProject1/translated.csv"
#     df.to_csv(translated_path, index=False)
#
#     # 訓練模型
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model = BERTClassifier(model_name='bert-base-chinese', num_labels=6).to(device)
#     optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
#
#     text_column = "translated_text"
#     label_columns = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
#
#     train_loader, val_loader = prepare_dataloader_from_csv(
#         df = df,
#         text_column=text_column,
#         label_columns=label_columns,
#         tokenizer_name='bert-base-chinese',
#         batch_size=16,
#         max_length=128,
#         val_size=0.2
#     )
#
#     train_model(model, train_loader, val_loader, optimizer, device, num_epochs=10)
#
#     # 儲存模型與 tokenizer
#     os.makedirs("bert_model/Saved_model", exist_ok=True)
#     torch.save(model.state_dict(), "bert_model/Saved_model/pytorch_model.bin")
#
#     tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
#     tokenizer.save_pretrained("bert_model/Saved_model")
#
#     config = {
#         "model_type": "bert",
#         "num_labels": 6
#     }
#     with open("bert_model/Saved_model/config.json", "w", encoding="utf-8") as f:
#         json.dump(config, f, ensure_ascii=False, indent=2)
#
#     print(f"\n🏁 全部流程完成，耗時：{time.time() - start_time:.2f} 秒")
#
# # -------------------------------
# if __name__ == "__main__":
#     main()