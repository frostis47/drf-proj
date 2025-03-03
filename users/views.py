
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, PaymentSerializer
from .models import Payment
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PaymentFilter


class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']