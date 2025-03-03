from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from lms import views

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='courses')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('api/', include('lms.urls')),
]