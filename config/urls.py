from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from lms import views

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('lms.urls')), # Подключаем urls приложения lms
    path('api/users/', include('users.urls')),
]