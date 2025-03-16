from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Банковский перевод'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата платежа')
    paid_course = models.ForeignKey('lms.Course', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey('lms.Lesson', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Оплаченный урок')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Сумма платежа')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    def __str__(self):
        return f"Платеж от {self.user.email} {self.payment_date}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'




class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'