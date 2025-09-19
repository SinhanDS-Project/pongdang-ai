import pandas as pd
import joblib
import numpy as np

# --------------------
# 1. 모델 로드
# --------------------
kmeans = joblib.load("models/kmeans_model.pkl")
tree = joblib.load("models/tree_model.pkl")
scaler = joblib.load("models/scaler.pkl")
loan_map = joblib.load("models/loan_map.pkl")
invest_map = joblib.load("models/invest_map.pkl")

# --------------------
# 2. 클러스터 라벨
# --------------------
cluster_labels = {
    0: "균형형",
    1: "투자형",
    2: "소비형",
    3: "절약형"
}

# --------------------
# 3. 예측 함수
# --------------------
def generate_report(user_input: dict):
    df_new = pd.DataFrame([user_input])

    # 파생 변수 계산
    df_new["spend_rate"] = df_new["spend"] / df_new["income"]
    df_new["saving_rate"] = (df_new["income"] - df_new["spend"]) / df_new["income"]
    df_new["goal_achieve"] = df_new["current_saving"] / df_new["saving_goal"]

    # 매핑 처리
    df_new["loan"] = df_new["loan"].map(loan_map)
    df_new["invest_type"] = df_new["invest_type"].map(invest_map)

    # KMeans (군집 예측)
    numeric_cols = ["age","income","spend","saving_goal","current_saving",
                    "spend_rate","saving_rate","goal_achieve"]
    X_scaled = scaler.transform(df_new[numeric_cols])
    cluster = kmeans.predict(X_scaled)[0]
    cluster_name = cluster_labels.get(cluster, f"Unknown-{cluster}")

    # Decision Tree (전략 예측)
    features = ["income", "spend_rate", "saving_rate", "goal_achieve", "loan", "invest_type"]
    strategy = tree.predict(df_new[features])[0]

    # --------------------
    # 리포트 작성
    # --------------------
    report = f"""
[개인 금융 리포트]

- 나이: {user_input['age']}세
- 월 소득: {user_input['income']:,}원
- 월 소비: {user_input['spend']:,}원 (소득 대비 {df_new['spend_rate'].iloc[0]*100:.1f}%)
- 저축 목표액: {user_input['saving_goal']:,}원
- 현재 저축액: {user_input['current_saving']:,}원 (목표 달성률 {df_new['goal_achieve'].iloc[0]*100:.1f}%)
- 부채 여부: {"있음" if user_input['loan']=="있음" else "없음"}
- 투자 성향: {user_input['invest_type']}
- 목표 기간: {user_input['goal_term']}

[분석 결과]
▶ KMeans 그룹: {cluster_name} : Cluster {cluster}
▶ Decision Tree 전략: {strategy}
"""
    return report

# --------------------
# 4. 테스트 실행
# --------------------
if __name__ == "__main__":
    new_user = {
        "age": 41,
        "income": 6000000,          # 월 소득 350만원
        "spend": 4500000,           # 월 소비 300만원
        "saving_goal": 10000000000,   # 목표 저축액 1억
        "main_category": "주거·관리",
        "current_saving": 50000000, # 현재 저축액 8천만원
        "loan": "있음",
        "invest_type": "안정형",
        "goal_term": "중기"
    }

    print(generate_report(new_user))
