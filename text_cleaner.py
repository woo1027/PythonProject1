import re


def clean_text(text):
    text = text.lower() #轉小寫 避免混淆、減少維度
    text = re.sub(r"what's", "what is ", text) #將what's替換成what is
    text = re.sub(r"\'s", " ", text) # 確保文本可以完整形式呈現，有助於提高模型理解
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text) #以上皆是將縮寫展開
    text = re.sub(r'http\S+|www\S+|https\S+', '', text) #移除http
    text = re.sub(r'<[^>]+>', '', text) #移除HTML
    #這些網址對NLP沒有意義
    text = re.sub('\W', ' ', text) #將非字母、數字轉換為空格
    text = re.sub('\s+', ' ', text) #將多個空格轉為一個空格
    text = text.strip(' ') #去除開頭以及結尾的空格
    return text