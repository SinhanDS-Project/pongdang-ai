import pandas as pd
import random

categories = [
    "주거·관리비","식비·외식","교통·차량","의류·쇼핑",
    "의료·건강","교육·자기계발","여가·문화","금융·투자",
    "통신·인터넷","기타지출"
]
invest_types = ["안정형", "중립형", "공격형"]
goal_terms = ["단기", "중기", "장기"]

data = []

# 전체 5000개 더미 데이터
n = 5000
group_size = n // 5  # 그룹당 약 1000개씩

# ----------------------------
# Group A: 소비형 (소비↑, 저축↓)
# ----------------------------
for _ in range(group_size):
    income = random.randint(200, 600) * 10000  # 소득 200~600만
    spend = int(income * random.uniform(0.7, 0.9))  # 소비율 70~90%
    saving_goal = random.randint(500, 2000) * 10000
    current_saving = random.randint(0, int(income*6))  # 저축 낮음
    data.append([
        random.randint(20, 45), income, spend, saving_goal,
        random.choice(categories), current_saving, "없음",
        random.choice(["중립형", "안정형"]), random.choice(goal_terms), "소비형"
    ])

# ----------------------------
# Group B: 절약형 (소비↓, 저축↑)
# ----------------------------
for _ in range(group_size):
    income = random.randint(200, 600) * 10000
    spend = int(income * random.uniform(0.3, 0.5))  # 소비율 30~50%
    saving_goal = random.randint(1000, 5000) * 10000
    current_saving = random.randint(int(income*12), int(income*36))  # 저축 많음
    data.append([
        random.randint(25, 55), income, spend, saving_goal,
        random.choice(categories), current_saving, "없음",
        random.choice(["안정형", "중립형"]), random.choice(goal_terms), "절약형"
    ])

# ----------------------------
# Group C: 투자형 (고소득, 공격적 투자)
# ----------------------------
for _ in range(group_size):
    income = random.randint(600, 1200) * 10000  # 고소득
    spend = int(income * random.uniform(0.5, 0.7))
    saving_goal = random.randint(2000, 20000) * 10000
    current_saving = random.randint(int(income*6), int(income*24))
    data.append([
        random.randint(30, 50), income, spend, saving_goal,
        "금융·투자", current_saving, "없음",
        "공격형", random.choice(goal_terms), "투자형"
    ])

# ----------------------------
# Group D: 균형형 (소비≈저축)
# ----------------------------
for _ in range(group_size):
    income = random.randint(300, 800) * 10000
    spend = int(income * random.uniform(0.45, 0.55))  # 소비≈저축
    saving_goal = random.randint(1000, 10000) * 10000
    current_saving = random.randint(int(income*6), int(income*18))
    data.append([
        random.randint(25, 55), income, spend, saving_goal,
        random.choice(categories), current_saving, "없음",
        random.choice(invest_types), random.choice(goal_terms), "균형형"
    ])

# ----------------------------
# Group E: 부채형 (소비↑, 부채 있음, 저축↓)
# ----------------------------
for _ in range(group_size):
    income = random.randint(200, 600) * 10000
    spend = int(income * random.uniform(0.6, 0.8))  # 소비 높음
    saving_goal = random.randint(500, 5000) * 10000
    current_saving = random.randint(0, int(income*6))  # 저축 낮음
    data.append([
        random.randint(20, 50), income, spend, saving_goal,
        random.choice(categories), current_saving, "있음",
        random.choice(invest_types), random.choice(goal_terms), "부채형"
    ])

# ----------------------------
# DataFrame 저장
# ----------------------------
df = pd.DataFrame(data, columns=[
    "age","income","spend","saving_goal",
    "main_category","current_saving","loan",
    "invest_type","goal_term","true_group"   # 정답 라벨
])

df.to_csv("survey_dummy_data.csv", index=False, encoding="utf-8-sig")
print("✅ 그룹 기반 더미 데이터 5000개 생성 완료!")
