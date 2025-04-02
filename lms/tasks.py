from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import CourseSubscription, Course
from django.utils import timezone
from datetime import timedelta
@shared_task
def send_course_update_email(course_id):
    """
    Асинхронно отправляет email подписчикам при обновлении курса.

    Args:
        course_id (int): ID обновленного курса.

    Returns:
        str: Сообщение об успехе или неудаче отправки email.
    """
    try:
        course = Course.objects.get(pk=course_id)  # Получаем объект курса из базы данных по ID
        time_difference = timezone.now() - course.last_update  # Вычисляем разницу между текущим временем и временем последнего обновления курса

        if time_difference < timedelta(hours=4):  # Проверяем, прошло ли больше 4 часов с момента последнего обновления
            return f"Skipped sending update email for course {course_id}: Updated too recently"  # Если прошло меньше 4 часов, возвращаем сообщение об отмене отправки

        subscriptions = CourseSubscription.objects.filter(course_id=course_id)  # Получаем всех подписчиков на данный курс
        email_list = [sub.user.email for sub in subscriptions]  # Формируем список email-адресов подписчиков

        send_mail(
            subject=f'Обновление курса!',  # Тема письма
            message=f'Курс с id {course_id} был обновлен. Проверьте новые материалы!',  # Сообщение письма
            from_email=settings.DEFAULT_FROM_EMAIL,  # Email отправителя берется из настроек Django
            recipient_list=email_list,  # Список email-адресатов
            fail_silently=False,
        )
        return f"Successfully sent update email to {len(email_list)} subscribers for course {course_id}"  # Возвращаем сообщение об успешной отправке

    except Course.DoesNotExist:  # Обрабатываем исключение, если курс с указанным ID не найден
        return f"Course with id {course_id} not found"  # Возвращаем сообщение о том, что курс не найден

    except Exception as e:  # Обрабатываем все остальные исключения
        return f"Failed to send update email for course {course_id}: {str(e)}"  # Возвращаем сообщение о неудачной отправке и текст ошибки