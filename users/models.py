from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings

class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватарка')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Банковский перевод'),
        ('stripe', 'Stripe'),  # Добавим Stripe
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка оплаты'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    course = models.ForeignKey('lms.Course', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный курс')
    lesson = models.ForeignKey('lms.Lesson', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты', default=0.00)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    # Stripe fields
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe Product ID')
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe Price ID')
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe Session ID')
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='Статус платежа'
    )


    def __str__(self):
        return f"Payment by {self.user} on {self.payment_date}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Пользователь')
    course = models.ForeignKey('lms.Course', on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Курс')

    def __str__(self):
        return f"Subscription: {self.user} -> {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
