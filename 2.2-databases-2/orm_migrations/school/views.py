from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'group'

    # Получаем всех учеников, сортируем их по группе и оптимизируем запрос к учителям
    students = Student.objects.all().order_by(ordering).prefetch_related('teachers')

    # Передаем полученную выборку в контекст шаблона
    # (в HTML-шаблоне список обычно ожидается под ключом 'object_list' или 'students')
    context = {
        'object_list': students
    }

    return render(request, template, context)
