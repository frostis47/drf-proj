from django.db import models

class Course(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название курса", help_text="Укажите название курса"
    )
    image = models.ImageField(
        upload_to="media/images", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )
    price = models.IntegerField(verbose_name="Цена", blank=True, null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="Укажите название урока"
    )
    image = models.ImageField(
        upload_to="media/images", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Укажите курс",
    )

    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Введите URL-адрес видео для урока (необязательно).",
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )
    price = models.IntegerField(verbose_name="Цена", blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscription_user",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscription_course",
    )
    is_subscribe = models.BooleanField(default=False, verbose_name="подписка")

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
