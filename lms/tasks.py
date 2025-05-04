from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lms.models import Subscription
from users.models import User


@shared_task
def mail_update_course_info(course_id):
    """Отправка сообщения об обновлении курса по подписке"""
    subscription_course = Subscription.objects.filter(course=course_id)
    print(f"Найдено {len(subscription_course)} подписок на курс {course_id}")
    for subscription in subscription_course:
        print(f"Отправка электронного письма на {subscription.user.email}")
        send_mail(
            subject="Обновление материалов курса",
            message=f"Курс {subscription.course.title} был обновлен.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )


@shared_task
def check_last_login():
    """Проверка последнего входа пользователей и отключение неактивных пользователей"""
    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f"Пользователь {user.email} отключен")
        else:
            print(f"Пользователь {user.email} активен")