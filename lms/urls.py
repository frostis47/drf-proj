from django.urls import path
from . import views

from .views import LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView

urlpatterns = [
    path('api/lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('api/lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('api/lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('api/lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('api/lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
]