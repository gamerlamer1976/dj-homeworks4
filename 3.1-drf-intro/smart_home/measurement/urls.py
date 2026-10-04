from django.urls import path
from .views import SensorView, SensorUpdateView, MeasurementCreateView

urlpatterns = [
    # Список датчиков и создание датчика
    path('sensors/', SensorView.as_view()),

    # Получение, обновление конкретного датчика по его ID (в Django это называется pk - primary key)
    path('sensors/<pk>/', SensorUpdateView.as_view()),

    # Добавление нового измерения температуры
    path('measurements/', MeasurementCreateView.as_view()),
]
