from data_loader import load_data, save_data
from text_cleaner import clean_text
from translator import translate_to_chinese
import time


def main():
    start_time = time.time()  # 記錄開始時間

    df = load_data("C:/Users/user/Downloads/t.csv")
    df['clean_text'] = df['comment_text'].map(clean_text)
    df['translated_text'] = df['clean_text'].map(translate_to_chinese)
    save_data(df, "C:/Users/user/PycharmProjects/PythonProject1/translated.csv")

    end_time = time.time()  # 記錄結束時間
    elapsed_time = end_time - start_time
    print(f"處理完成，總共耗時：{elapsed_time:.2f} 秒")

if __name__ == "__main__":
    main()
