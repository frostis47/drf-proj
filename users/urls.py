from django.urls import path
from .views import UserProfileUpdateView, PaymentListView

urlpatterns = [
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]