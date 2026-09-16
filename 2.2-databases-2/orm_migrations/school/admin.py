from django.contrib import admin

from .models import Student, Teacher


# Создаем Inline-класс для скрытой промежуточной таблицы связи ученика и учителя[cite: 3]
class StudentTeacherInline(admin.TabularInline):
    model = Student.teachers.through
    extra = 1  # Количество дополнительных пустых строк для добавления[cite: 3]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    # Исключаем стандартное поле выбора, чтобы оно не дублировалось с Inline-панелью[cite: 3]
    exclude = ('teachers',)
    inlines = [
        StudentTeacherInline,
    ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    inlines = [
        StudentTeacherInline,
    ]
