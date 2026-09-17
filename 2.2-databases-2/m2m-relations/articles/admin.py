from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_count = 0

        for form in self.forms:
            # form.cleaned_data содержит данные, введенные в одну строку (форму)
            # Если форма пустая или помечена на удаление (DELETE), пропускаем её
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                if form.cleaned_data.get('is_main'):
                    main_count += 1

        # Проверки по условиям задачи
        if main_count == 0:
            raise ValidationError('Укажите основной раздел.')
        elif main_count > 1:
            raise ValidationError('Основным может быть только один раздел.')

        return super().clean()  # Обязательно вызываем базовый метод


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1  # Количество дополнительных пустых строк по умолчанию


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
