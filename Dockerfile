FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV SECRET_KEY= django-insecure-zxxr5=0g_+v-a)&x$4^s+k9jg+p99ub0gvow%5del)l63=%w!c
ENV CELERY_BROKER_URL = f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/{os.getenv("REDIS_DB")}'
ENV CELERY_RESULT_BACKEND = f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/{os.getenv("REDIS_DB")}'
ENV DJANGO_SETTINGS_MODULE=config.settings

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

