FROM python:3.12-alpine

RUN addgroup -S group_savebit && adduser -S -G group_savebit userbit

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/web
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER userbit

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]