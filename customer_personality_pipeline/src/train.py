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

    results = []

    for name, model in models.items():
        print(f"\n==== Training {name.upper()} ====")
        scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
        mean_acc = scores.mean()
        std_acc = scores.std()
        print(f"{name} CV Accuracy: {mean_acc:.4f} ± {std_acc:.4f}")

        # 儲存模型資訊
        results.append((name, mean_acc, std_acc))

        # 訓練整體資料並儲存模型
        model.fit(X, y)
        joblib.dump(model, f"outputs/models/{name}.pkl")

        # 根據平均準確度排序
    results.sort(key=lambda x: x[1], reverse=True)

    print("\n===== Top 3 Models by Cross-Validation Accuracy =====")
    for rank, (name, mean_acc, std_acc) in enumerate(results[:3], start=1):
        print(f"{rank}. {name} - Accuracy: {mean_acc:.4f} ± {std_acc:.4f}")

if __name__ == '__main__':
    train_all_models_with_cv()