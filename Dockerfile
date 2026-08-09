FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY db ./db

EXPOSE 5000

CMD ["sh", "-c", "exec python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000} --proxy-headers --forwarded-allow-ips='*'"]
