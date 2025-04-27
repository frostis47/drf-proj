import django_filters
from .models import Payment



class PaymentFilter(django_filters.FilterSet):
    paid_course = django_filters.NumberFilter(field_name='paid_course__id')
    paid_lesson = django_filters.NumberFilter(field_name='paid_lesson__id')
    payment_amount = django_filters.NumberFilter(field_name='payment_amount')

    class Meta:
        model = Payment
        fields = ['user', 'payment_date', 'payment_method']
