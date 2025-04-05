from django.urls import path, include
from rest_framework import routers
from . import views
from .views import (CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView,
                    LessonDestroyAPIView, CreatePaymentView, CourseUpdateAPIView)

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='courses')


urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', views.LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lessons/create/', views.LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('payments/create/', views.CreatePaymentView.as_view(), name='create-payment'),
    path('courses/<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course-update'),
]
