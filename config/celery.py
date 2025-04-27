import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

app = Celery('your_project_name')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # Автоматически обнаруживаем и регистрируем Celery tasks во всех установленных Django apps


@app.task(bind=True)  # Регистрируем функцию debug_task как Celery task
def debug_task(self):
    """
    Celery task для отладки. Выводит информацию о запросе.
    """
    print(f'Request: {self.request!r}')  # Выводим информацию о запросе
