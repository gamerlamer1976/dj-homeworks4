from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # Фильтр для даты создания
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        # Указываем поля, по которым разрешена фильтрация
        fields = ['created_at', 'status']
