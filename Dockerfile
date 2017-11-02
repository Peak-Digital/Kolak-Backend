FROM python:2

RUN pip install gunicorn falcon aylien_news_api

WORKDIR /app

ENTRYPOINT gunicorn -b 0.0.0.0:5000 main:api --reload
