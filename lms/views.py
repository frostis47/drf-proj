from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import CustomPagination
from lms.serializers import (CourseDigtalSerializer, CourseSerializer,
                             LessonSerializer, SubscriptionSerializer)
from lms.tasks import mail_update_course_info
from users.permissions import IsModern, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    filterset_fields = ("lesson",)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDigtalSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModern,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = IsModern | IsOwner
        elif self.action == "destroy":
            self.permission_classes = ~IsModern | IsOwner
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        updated_course = serializer.save()
        mail_update_course_info.delay(updated_course)
        updated_course.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filterset_fields = ("course",)
    pagination_class = CustomPagination


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModern, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModern | IsOwner,
    )


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | ~IsModern, IsAuthenticated)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModern | IsOwner,
    )


class SubscriptionAPIView(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "Вы отписались"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Вы подписались"
        return Response({"message": message})


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
