from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.models import Payment
from .services import create_stripe_product, create_stripe_price, create_stripe_session
from .tasks import send_course_update_email


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class CreatePaymentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course')

        try:
            course = Course.objects.get(pk=course_id)
            amount = course.price
            payment_method = request.data.get('payment_method', 'stripe')

            # Создание или получение Stripe Product ID
            if not course.stripe_product_id:
                course.stripe_product_id = create_stripe_product(name=course.title)
                course.save()

            # Создание или получение Stripe Price ID
            if not course.stripe_price_id or course.price != course.stripe_price:
                course.stripe_price_id = create_stripe_price(product_id=course.stripe_product_id, amount=amount)
                course.stripe_price = amount
                course.save()

            success_url = settings.DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}'
            cancel_url = settings.DOMAIN + '/cancel'
            stripe_session_id, stripe_url = create_stripe_session(
                price_id=course.stripe_price_id,
                success_url=success_url,
                cancel_url=cancel_url
            )

            Payment.objects.create(
                user=request.user,
                payment_date=timezone.now(),
                course=course,
                amount=amount,
                payment_method=payment_method,
                stripe_product_id=course.stripe_product_id,
                stripe_price_id=course.stripe_price_id,
                stripe_session_id=stripe_session_id,
            )

            return Response({'stripe_url': stripe_url}, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseUpdateAPIView(generics.UpdateAPIView): # Added
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save() # Сохраняем изменения
        course = self.get_object() # Get the course object
        send_course_update_email.delay(course.id) # Вызов Celery task