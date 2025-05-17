FROM python:3.12

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода приложения
COPY . .

# Установка переменных окружения
ENV SECRET_KEY=${SECRET_KEY}
ENV CELERY_BROKER_URL=redis://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}
ENV CELERY_RESULT_BACKEND=redis://${REDIS_HOST}:${REDIS_PORT}/${REDIS_DB}
ENV DJANGO_SETTINGS_MODULE=config.settings

# Открытие порта для приложения
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
