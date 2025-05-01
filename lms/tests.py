from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lms.models import Course, Lesson
from users.models import User, Subscription
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group


class LMSAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.moderator = User.objects.create_user(email='moderator@example.com', password='moderatorpassword')
        moderator_group = Group.objects.create(name='moderators')
        self.moderator.groups.add(moderator_group)

        # Создаем токены
        self.user_token = self.get_token(self.user)
        self.moderator_token = self.get_token(self.moderator)

        # Создаем курсы и уроки
        self.course1 = Course.objects.create(title='Course 1', owner=self.user)
        self.lesson1 = Lesson.objects.create(title='Lesson 1', course=self.course1, owner=self.user)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token)}

    def test_course_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        data = {'title': 'New Course', 'description': 'Description'}
        response = self.client.post(reverse('course-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.last().title, 'New Course')
        self.assertEqual(Course.objects.last().owner, self.user)

    def test_course_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_course_update_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        data = {'title': 'Updated Course'}
        response = self.client.patch(reverse('course-detail', args=[self.course1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(pk=self.course1.pk).title, 'Updated Course')

    def test_course_update_by_not_owner(self):
        user2 = User.objects.create_user(email='test2@example.com', password='testpassword')
        token2 = self.get_token(user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2["access"]}')
        data = {'title': 'Updated Course by another user'}
        response = self.client.patch(reverse('course-detail', args=[self.course1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        data = {'title': 'New Lesson', 'course': self.course1.pk}
        response = self.client.post(reverse('lesson-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().title, 'New Lesson')
        self.assertEqual(Lesson.objects.last().course, self.course1)
        self.assertEqual(Lesson.objects.last().owner, self.user)

    def test_lesson_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_lesson_update_by_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(reverse('lesson-detail', args=[self.lesson1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(pk=self.lesson1.pk).title, 'Updated Lesson')

    def test_lesson_update_by_not_owner(self):
        user2 = User.objects.create_user(email='test2@example.com', password='testpassword')
        token2 = self.get_token(user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2["access"]}')
        data = {'title': 'Updated Lesson by another user'}
        response = self.client.patch(reverse('lesson-detail', args=[self.lesson1.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscription_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        data = {'course': self.course1.pk} # changed course_id to course
        response = self.client.post(reverse('subscriptions'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.first().user, self.user)
        self.assertEqual(Subscription.objects.first().course, self.course1)

    def test_subscription_list(self):
        Subscription.objects.create(user=self.user, course=self.course1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        response = self.client.get(reverse('subscriptions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.pk)
        self.assertEqual(response.data[0]['course'], self.course1.pk)

    def test_subscription_delete(self):
        subscription = Subscription.objects.create(user=self.user, course=self.course1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token["access"]}')
        response = self.client.delete(reverse('subscription-delete', args=[subscription.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)
