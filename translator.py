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
