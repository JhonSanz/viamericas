FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x init.sh

ENV DEBUG=False
ENV DJANGO_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "init.sh"]
