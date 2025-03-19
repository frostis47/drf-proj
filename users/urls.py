from django.urls import path
from .views import UserProfileUpdateView, PaymentListView, UserCreateView, UserListView, UserDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('profile/<int:pk>/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]