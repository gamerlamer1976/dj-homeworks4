from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Подключаем бэкенд для поиска
    filter_backends = [SearchFilter]
    # Настраиваем поиск продуктов по названию и описанию
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    # Подключаем бэкенды для фильтрации и поиска
    filter_backends = [DjangoFilterBackend, SearchFilter]

    # Основное задание: фильтрация складов, в которых есть определенный продукт, по ID
    filterset_fields = ['products']

    # Дополнительное задание: поиск складов по названию или описанию продукта
    search_fields = ['products__title', 'products__description']
