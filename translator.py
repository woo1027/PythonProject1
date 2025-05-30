from googletrans import Translator


translator = Translator()

def translate_to_chinese(text):
    try:
        # 使用googletrans進行翻譯，將src='en'設定為英文
        translation = translator.translate(text, src='en', dest='zh-tw')
        return translation.text
    except Exception as e:
        print(f"翻譯失敗: {e}")
        return text


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
