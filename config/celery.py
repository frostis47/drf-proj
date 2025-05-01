import os
from celery import Celery
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery
app = Celery('config')

# Загружаем конфигурацию Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """
    Celery task для отладки. Выводит информацию о запросе.
    """
    print(f'Request: {self.request!r}')

