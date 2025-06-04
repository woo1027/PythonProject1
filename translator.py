from googletrans import Translator
from tqdm import tqdm
import time

translator = Translator()

def translate_to_chinese(texts):
    translated_texts = []
    total = len(texts)

    print("🚀 開始翻譯...")

    for i, text in enumerate(tqdm(texts, desc="翻譯進度", unit="筆")):
        try:
            translation = translator.translate(text, src='en', dest='zh-tw')
            translated_texts.append(translation.text)
        except Exception as e:
            tqdm.write(f"❌ 第 {i+1} 筆翻譯失敗: {e}")
            translated_texts.append(text)  # 若失敗保留原文

        time.sleep(0.1)  # 小延遲，避免被封鎖

    return translated_texts

#
# def translate_to_chinese(texts, batch_size=200, delay=1.5):
#     translated_text = []
#     total = len(texts)
#
#     for i in range(0, total, batch_size):
#         batch = texts[i:i + batch_size]
#         translated_batch = []
#
#         print(f"📦 翻譯中: 第 {i} 至 {i + len(batch) - 1} 筆")
#
#         for text in batch:
#             try:
#                 translated = translator.translate(text, src='en', dest='zh-tw')
#                 translated_batch.append(translated.text)
#             except Exception as e:
#                 print(f"❌ 翻譯失敗: {e}")
#                 translated_batch.append(text)  # 若失敗，保留原文
#             time.sleep(0.1)  # 每筆稍作延遲以減輕API負擔
#
#         translated_text.extend(translated_batch)
#
#         # 顯示進度
#         percent = (i + len(batch)) / total * 100
#         print(f"✅ 目前進度: {i + len(batch)}/{total} ({percent:.2f}%)")
#
#         time.sleep(delay)  # 每個 batch 延遲
#
#     return translated_text


# from googletrans import Translator
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import time
#
#
# def translate_to_chinese(text_list, max_retries=3, max_workers=5):
#     """
#     將輸入的英文文字列表翻譯為繁體中文，支援多執行緒與錯誤重試機制。
#
#     :param text_list: 要翻譯的文字列表
#     :param max_retries: 每筆翻譯的最大重試次數
#     :param max_workers: 同時進行翻譯的執行緒數
#     :return: 翻譯後的文字列表
#     """
#
#     translator = Translator()
#
#     def translate_text(cell):
#         for attempt in range(max_retries):
#             try:
#                 translated = translator.translate(cell, dest='zh-tw')
#                 return translated.text
#             except Exception as e:
#                 print(f"[重試 {attempt + 1}/{max_retries}] 翻譯失敗: {e}")
#                 time.sleep(1)
#         return "翻譯失敗"
#
#     translations = []
#
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         future_to_text = {executor.submit(translate_text, text): text for text in text_list}
#
#         for future in as_completed(future_to_text):
#             result = future.result()
#             translations.append(result)
#
#     return translations
