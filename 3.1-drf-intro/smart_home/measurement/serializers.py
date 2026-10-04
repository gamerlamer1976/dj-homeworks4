from rest_framework import serializers
from .models import Sensor, Measurement

class MeasurementSerializer(serializers.ModelSerializer):
    """Сериализатор для измерений температуры."""
    class Meta:
        model = Measurement
        # Указываем поля, которые будут отдаваться и приниматься по API.
        # Поле sensor необходимо для того, чтобы при добавлении измерения
        # мы могли указать ID датчика (как требует ТЗ).
        fields = ['sensor', 'temperature', 'created_at', 'image']


class SensorSerializer(serializers.ModelSerializer):
    """Сериализатор для списка датчиков (краткая информация)."""
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации по датчику."""
    # Вложенный сериализатор для отображения списка измерений.
    # Имя переменной 'measurements' должно строго совпадать с related_name из models.py!
    # read_only=True означает, что мы только отдаем эти данные, но не изменяем их здесь.
    # many=True означает, что измерений может быть несколько (список).
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
