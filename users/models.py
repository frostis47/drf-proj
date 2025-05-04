from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создает и возвращает пользователя с электронной почтой и паролем."""
        if not email:
            raise ValueError("Пользователю необходимо указать адрес электронной почты")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и возвращает суперпользователя с электронной почтой и паролем."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Payments(models.Model):
    PAYMENT_METHOD = (
        ("cash", "наличные"),
        ("transfer", "перевод на счет"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Плательщик",
        help_text="Укажите плательщика",
    )
    payment_date = models.DateTimeField(
        verbose_name="Дата оплаты",
        help_text="Укажите дату оплаты",
        blank=True,
        null=True,
    )
    course_paid = models.ForeignKey(
        'lms.Course',  # Используйте строку вместо импорта
        on_delete=models.CASCADE,
        related_name="payments_course",
        verbose_name="Оплаченный курс",
        help_text="Укажите оплаченный курс",
        blank=True,
        null=True,
    )
    lesson_paid = models.ForeignKey(
        'lms.Lesson',  # Используйте строку вместо импорта
        on_delete=models.CASCADE,
        related_name="payments_lesson",
        verbose_name="Оплаченный урок",
        help_text="Укажите оплаченный урок",
        blank=True,
        null=True,
    )

    payment_amount = models.PositiveIntegerField(
        default=0,
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
        blank=True,
        null=True,
    )
    payment_method = models.CharField(
        choices=PAYMENT_METHOD,
        max_length=255,
        default="cash",
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
        blank=True,
        null=True,
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="Id сессии",
        blank=True,
        null=True,
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Cсылка на оплату",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user.email} - {self.payment_amount} руб."



