from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# ---------------------------
# FastAPI 앱 생성
# ---------------------------
app = FastAPI()

# ---------------------------
# 1. 모델 & 전처리 로드
# ---------------------------
kmeans = joblib.load("models/kmeans_model.pkl")
tree = joblib.load("models/tree_model.pkl")  # Decision Tree 로드
scaler = joblib.load("models/scaler.pkl")
encoders = joblib.load("models/encoders.pkl")

# ---------------------------
# 2. 입력 스키마 정의
# ---------------------------
class UserInput(BaseModel):
    age: int
    income: int
    spend: int
    main_category: str
    saving_goal: int
    current_saving: int
    loan: str
    invest_type: str
    goal_term: str

# ---------------------------
# 3. 군집 라벨 정의
# ---------------------------
cluster_labels = {
    0: "균형형",
    1: "투자형",
    2: "소비형",
    3: "절약형"
}

# ---------------------------
# 4. 예측 API
# ---------------------------
@app.post("/predict")
def predict(user: UserInput):
    # 입력값 DataFrame 변환
    df_new = pd.DataFrame([user.dict()])

    # 파생 변수 계산
    df_new["spend_rate"] = df_new["spend"] / df_new["income"]
    df_new["saving_rate"] = (df_new["income"] - df_new["spend"]) / df_new["income"]
    df_new["goal_achieve"] = df_new["current_saving"] / df_new["saving_goal"]

    # 범주형 인코딩
    for col in ["main_category", "loan", "invest_type", "goal_term"]:
        if col in encoders:
            df_new[col] = encoders[col].transform([df_new[col].iloc[0]])

    # 스케일링 (수치형 컬럼만 선택)
    numeric_cols = [
        "age", "income", "spend", "saving_goal", "current_saving",
        "spend_rate", "saving_rate", "goal_achieve"
    ]
    X_new = scaler.transform(df_new[numeric_cols])

    # KMeans 클러스터 예측
    cluster = kmeans.predict(X_new)[0]
    cluster_name = cluster_labels.get(cluster, "분류불가")

    # Decision Tree (전략 예측)
    features = ["income", "spend_rate", "saving_rate", "goal_achieve", "loan", "invest_type"]
    strategy = tree.predict(df_new[features])[0]

    # JSON 형태로 반환
    return {
        "cluster": int(cluster),
        "cluster_label": cluster_name,
        "spend_rate": round(df_new["spend_rate"].iloc[0] * 100, 1),
        "saving_rate": round(df_new["saving_rate"].iloc[0] * 100, 1),
        "goal_achieve": round(df_new["goal_achieve"].iloc[0] * 100, 1),
        "strategy": strategy
    }
