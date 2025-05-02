from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import CourseSubscription, Course
from django.utils import timezone
from datetime import timedelta
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

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
        course = Course.objects.get(pk=course_id)
        time_difference = timezone.now() - course.last_update

        if time_difference < timedelta(hours=4):
            logger.info(f"Skipped sending update email for course {course_id}: Updated too recently")
            return "Skipped sending update email: Updated too recently"

        subscriptions = CourseSubscription.objects.filter(course_id=course_id)
        email_list = [sub.user.email for sub in subscriptions]

        if not email_list:
            logger.info(f"No subscribers found for course {course_id}.")
            return "No subscribers to notify."

        send_mail(
            subject='Обновление курса!',
            message=f'Курс с id {course_id} был обновлен. Проверьте новые материалы!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email_list,
            fail_silently=False,
        )
        logger.info(f"Successfully sent update email to {len(email_list)} subscribers for course {course_id}")
        return f"Successfully sent update email to {len(email_list)} subscribers for course {course_id}"

    except Course.DoesNotExist:
        logger.error(f"Course with id {course_id} not found")
        return "Course not found"

    except Exception as e:
        logger.error(f"Failed to send update email for course {course_id}: {str(e)}")
        return f"Failed to send update email: {str(e)}"
