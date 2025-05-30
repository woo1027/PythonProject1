# src/model.py

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC

def build_models():
    return {
        "random_forest": RandomForestClassifier(random_state=42),
        "xgboost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
        "svc": SVC(probability=True, random_state=42),
        "logistic_regression": LogisticRegression(max_iter=1000),
        "knn": KNeighborsClassifier(n_neighbors=5),
        "naive_bayes": GaussianNB(),
        "decision_tree": DecisionTreeClassifier(random_state=42),
        "lightgbm": LGBMClassifier(),
        "catboost": CatBoostClassifier(verbose=0)
    }
