# src/train.py

import joblib
import os
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score
from customer_personality_pipeline.src.data_loader import load_data
from customer_personality_pipeline.src.preprocessing import preprocess
from customer_personality_pipeline.src.model import build_models

def train_all_models_with_cv():
    df = preprocess(load_data())

    # 特徵與標籤
    X = df[['Age', 'Income', 'Recency', 'TotalSpend', 'Customer_For', 'Children']]
    y = df['Response']

    models = build_models()
    os.makedirs("outputs/models", exist_ok=True)

    # 定義交叉驗證策略
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        print(f"\n==== Training {name.upper()} ====")

        # 交叉驗證
        scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        print(f"{name} CV Accuracy: {scores.mean():.4f} ± {scores.std():.4f}")

        # 使用全部資料訓練最終模型並儲存
        model.fit(X, y)
        joblib.dump(model, f"outputs/models/{name}.pkl")

if __name__ == '__main__':
    train_all_models_with_cv()