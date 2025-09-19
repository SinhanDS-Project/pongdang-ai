import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
import joblib

# --------------------
# 1. 데이터 불러오기
# --------------------
df = pd.read_csv("survey_dummy_data.csv")

# --------------------
# 2. 범주형 매핑
# --------------------
loan_map = {"없음": 0, "있음": 1}
invest_map = {"안정형": 0, "중립형": 1, "공격형": 2}

df["loan"] = df["loan"].map(loan_map)
df["invest_type"] = df["invest_type"].map(invest_map)

# --------------------
# 3. 파생 변수
# --------------------
df["spend_rate"] = df["spend"] / df["income"]
df["saving_rate"] = (df["income"] - df["spend"]) / df["income"]
df["goal_achieve"] = df["current_saving"] / df["saving_goal"]

# --------------------
# 4. KMeans 군집화 (참고용)
# --------------------
numeric_cols = ["age","income","spend","saving_goal","current_saving",
                "spend_rate","saving_rate","goal_achieve"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[numeric_cols])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

# --------------------
# 5. 전략 라벨링 (규칙 기반)
# --------------------
strategies = []
for _, row in df.iterrows():
    if row["spend_rate"] > 0.8:
        strategies.append("소비절감필요")
    elif row["saving_rate"] > 0.3 and row["invest_type"] == 2:  # 공격형
        strategies.append("투자확대권장")
    elif row["loan"] == 1 and row["spend_rate"] > 0.7:
        strategies.append("부채관리필요")
    elif row["goal_achieve"] < 0.1:
        strategies.append("목표강화필요")
    else:
        strategies.append("균형전략")

df["strategy"] = strategies

# --------------------
# 6. 의사결정나무 학습 (분류)
# --------------------
features = ["income", "spend_rate", "saving_rate", "goal_achieve", "loan", "invest_type"]
X = df[features]
y = df["strategy"]

tree = DecisionTreeClassifier(max_depth=4, random_state=42)
tree.fit(X, y)

# --------------------
# 7. 모델 저장
# --------------------
joblib.dump(kmeans, "models/kmeans_model.pkl")
joblib.dump(tree, "models/tree_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(loan_map, "models/loan_map.pkl")
joblib.dump(invest_map, "models/invest_map.pkl")

print("KMeans + DecisionTree 모델 학습 & 저장 완료!")
