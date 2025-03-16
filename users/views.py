from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Payment
from .serializers import PaymentSerializer, UserSerializer
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PaymentFilter


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
