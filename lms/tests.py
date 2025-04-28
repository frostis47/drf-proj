from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Course, Lesson, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(title="moderator", description="Test")  # Изменено на title
        self.lesson = Lesson.objects.create(
            title="Django", course=self.course, owner=self.user  # Изменено на title
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse("lms:lesson_create")
        data = {
            "title": "Test",  # Изменено на title
            "description": "Test",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_with_youtube(self):
        url = reverse("lms:lesson_create")
        data = {
            "title": "Test",  # Изменено на title
            "description": "Test",
            "course": self.course.pk,
            "owner": self.user.pk,
            "video_link": "https://www.youtube.com/",  # Изменено на video_link
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_invalid_youtube(self):
        url = reverse("lms:lesson_create")
        data = {
            "title": "Test",  # Изменено на title
            "description": "Test",
            "course": self.course.pk,
            "owner": self.user.pk,
            "video_link": "https://www.vk.com/",  # Изменено на video_link
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update(self):
        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "Test1",  # Изменено на title
            "description": "Test1",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), "Test1")  # Изменено на title

    def test_lesson_delete(self):
        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(name="moderator", description="Test")
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        Subscription.objects.all().delete()
        url = reverse("lms:subscription_create")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Вы подписались")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # Проверка отписки
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Вы отписались")

    def test_subscription_list(self):
        url = reverse("lms:subscription_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["course"], self.course.id)

    def test_subscribe_to_course_no_ex(self):
        Subscription.objects.all().delete()
        url = reverse("lms:subscription_create")
        data = {"course_id": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_to_course_no_au(self):
        Subscription.objects.all().delete()
        self.client.force_authenticate(user=None)
        url = reverse("lms:subscription_create")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
