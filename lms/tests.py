from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lms.models import Course, Lesson, Subscription
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model  # Import get_user_model

User = get_user_model()


class LMSAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword')

        # Create a course
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)

        # Create a lesson associated with the course
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Lesson', course=self.course,
                                            owner=self.user)

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_course_create(self):
        url = reverse('course-list')
        data = {'title': 'New Course', 'description': 'New Description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(),
                         2)
        self.assertEqual(Course.objects.last().title, 'New Course')

    def test_course_list(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Course')

    def test_subscription_create(self):
        url = reverse('subscription-create')
        data = {'user': self.user.pk, 'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_subscription_list(self):
        # Create a subscription
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('subscription-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.pk)
        self.assertEqual(response.data[0]['course'], self.course.pk)

    def test_subscription_delete(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('subscription-delete', args=[subscription.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Lesson')

    def test_lesson_update_by_owner(self):
        url = reverse('lesson-detail', args=[self.lesson.pk])
        data = {'title': 'Updated Test Lesson', 'description': 'Updated Test Lesson'}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(pk=self.lesson.pk).title, 'Updated Test Lesson')

    def test_lesson_update_not_owner(self):
        url = reverse('lesson-detail', args=[self.lesson.pk])
        data = {'title': 'Updated Test Lesson', 'description': 'Updated Test Lesson'}
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_owner(self):
        url = reverse('lesson-detail', args=[self.lesson.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_delete_not_owner(self):
        url = reverse('lesson-detail', args=[self.lesson.pk])
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
