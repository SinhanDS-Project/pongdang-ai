import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans

# -------------------------
# 1. 데이터 불러오기
# -------------------------
df = pd.read_csv("survey_dummy_data.csv")

# -------------------------
# 2. 범주형 → 숫자 인코딩
# -------------------------
label_cols = ["main_category", "loan", "invest_type", "goal_term"]
encoders = {}

for col in label_cols:
    enc = LabelEncoder()
    df[col] = enc.fit_transform(df[col])
    encoders[col] = enc

# -------------------------
# 3. 파생 변수 계산
# -------------------------
df["spend_rate"] = df["spend"] / df["income"]
df["saving_rate"] = (df["income"] - df["spend"]) / df["income"]
df["goal_achieve"] = df["current_saving"] / df["saving_goal"]

# -------------------------
# 4. 스케일링 + KMeans
# -------------------------
numeric_cols = ["age","income","spend","saving_goal","current_saving",
                "spend_rate","saving_rate","goal_achieve"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[numeric_cols])

# 클러스터 개수 (예: 4개 그룹)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

# -------------------------
# 5. 클러스터별 평균값 요약
# -------------------------
cluster_summary = df.groupby("cluster")[
    ["age","income","spend","spend_rate","saving_rate",
     "goal_achieve","current_saving"]
].mean().round(2)

print("\n클러스터별 평균값")
print(cluster_summary)

print("\n모델과 인코더 저장 완료!")
