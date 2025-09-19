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

for _ in range(5000):
    # 나이
    age = random.randint(15, 55)

    # 월 소득 (200만 ~ 1000만, 나이에 따라 평균 상향)
    base_income = random.randint(200, 600) if age < 30 else random.randint(300, 1000)
    income = base_income * 10000

    # 월 소비 (소득의 40~80%)
    spend_ratio = random.uniform(0.4, 0.8)
    spend = int(income * spend_ratio)

    # 저축 목표액 (소득 × 몇 개월분, 보통 1천만 ~ 2억)
    saving_goal = random.randint(12, 60) * income  # 1~5년치 소득
    saving_goal = min(saving_goal, 200000000)  # 2억 상한

    # 현재 저축액 (소득 × 0~36개월분, 목표 대비 최대 70%)
    current_saving = random.randint(0, int(income * 36))
    current_saving = min(current_saving, int(saving_goal * 0.7))

    # 주요 소비 항목 (소득·나이에 따라 경향)
    if age < 25:
        main_category = random.choice(["식비·외식","의류·쇼핑","여가·문화","금융·투자"])
    elif age < 40:
        main_category = random.choice(["주거·관리비","식비·외식","교통·차량","여가·문화"])
    else:
        main_category = random.choice(["주거·관리비","교육·자기계발","의료·건강","금융·투자"])

    # 부채 여부 (소득이 낮을수록, 나이가 어릴수록 확률 ↑)
    loan = "있음" if random.random() < (0.4 if income < 4000000 else 0.2) else "없음"

    # 투자 성향 (나이가 많을수록 안정형, 젊을수록 공격형 확률 ↑)
    if age < 30:
        invest_type = random.choices(invest_types, weights=[1, 2, 3])[0]
    elif age < 45:
        invest_type = random.choices(invest_types, weights=[2, 3, 2])[0]
    else:
        invest_type = random.choices(invest_types, weights=[3, 2, 1])[0]

    # 목표 기간 (나이가 어릴수록 장기, 많을수록 단기 선호)
    if age < 30:
        goal_term = random.choices(goal_terms, weights=[1, 2, 3])[0]
    elif age < 45:
        goal_term = random.choices(goal_terms, weights=[2, 3, 2])[0]
    else:
        goal_term = random.choices(goal_terms, weights=[3, 2, 1])[0]

    data.append([
        age, income, spend, saving_goal,
        main_category, current_saving, loan,
        invest_type, goal_term
    ])

df = pd.DataFrame(data, columns=[
    "age","income","spend","saving_goal",
    "main_category","current_saving","loan",
    "invest_type","goal_term"
])

df.to_csv("survey_dummy_data.csv", index=False, encoding="utf-8-sig")
print("✅ 더미 데이터 생성 완료!")
