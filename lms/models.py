from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview_image = models.ImageField(
        upload_to="courses/previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание курса"
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание урока"
    )
    preview_image = models.ImageField(
        upload_to="lessons/previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение ",
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="Введите ссылку на видео",
    )

    course = models.ForeignKey(
        "Course", related_name="lessons", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


