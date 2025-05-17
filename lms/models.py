from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название курса", help_text="Укажите название курса"
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name="URL")
    image = models.ImageField(
        upload_to="courses/images/", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )
    discount = models.IntegerField(
        verbose_name="Скидка",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]

class Lesson(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="Укажите название урока"
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name="URL")
    image = models.ImageField(
        upload_to="lessons/images/", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
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
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )
    order = models.IntegerField(
        verbose_name="Порядок",
        default=0,
        help_text="Порядок отображения урока в курсе",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        blank=True,
        null=True,
        validators=[MinValueValidator(0.00)],
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["order"]

class Subscription(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscription_user",
        db_index=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscription_course",
        db_index=True,
    )
    is_subscribe = models.BooleanField(default=False, verbose_name="подписка")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата окончания")

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")