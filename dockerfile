FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DEBUG=True
ENV DJANGO_ENV=development
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "init.sh"]
