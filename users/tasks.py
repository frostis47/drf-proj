from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

@shared_task  # Преобразуем функцию block_inactive_users в Celery task
def block_inactive_users():
    """
    Celery task для блокировки пользователей, не заходивших в систему более месяца.
    """
    User = get_user_model()  # Получаем модель User
    cutoff_date = timezone.now() - timedelta(days=30)  # Вычисляем дату, после которой пользователи считаются неактивными (30 дней назад)
    inactive_users = User.objects.filter(last_login__lt=cutoff_date, is_active=True)  # Получаем всех активных пользователей

    for user in inactive_users:  # Итерируем по списку неактивных пользователей
        user.is_active = False  # Устанавливаем  is_active в False,блокируем пользователя
        user.save()  # Сохраняем изменения в базе данных
        print(f"User {user.email} blocked due to inactivity.")  # Выводим сообщение о блокировке пользователя

    return f"Blocked {inactive_users.count()} inactive users."  # Возвращаем сообщение о количестве заблокированных пользователей