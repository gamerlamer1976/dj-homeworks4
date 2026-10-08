from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, attrs):
        # Получаем список студентов из входящих данных
        students = attrs.get('students')

        # Проверяем, что студенты вообще переданы в запросе (чтобы не сломать PATCH-запросы),
        # и что их количество не превышает заданный в настройках лимит
        if students is not None and len(students) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(
                f"Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}"
            )

        return attrs
