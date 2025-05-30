import pandas as pd

def load_data():
    df = pd.read_csv("C:/Users/user/PycharmProjects/PythonProject1/customer_personality_pipeline/marketing_campaign.csv", sep="\t")
    df = df.dropna()
    return df

