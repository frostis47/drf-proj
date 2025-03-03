
import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    payment_date = django_filters.DateFromToRangeFilter()
    course = django_filters.NumberFilter(field_name='course__id')
    lesson = django_filters.NumberFilter(field_name='lesson__id')
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHODS)
    class Meta:
        model = Payment
        fields = ['payment_date', 'course', 'lesson', 'payment_method']