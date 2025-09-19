FROM python:3.11-slim

# 기본 설정(로그 버퍼링/pyc 미생성)
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# 파이썬 의존성
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 소스
COPY . .

EXPOSE 8000

CMD ["uvicorn", "ml_api:app", "--host", "0.0.0.0", "--port", "8000"]
