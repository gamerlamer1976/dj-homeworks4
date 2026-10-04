from rest_framework import generics
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorView(generics.ListCreateAPIView):
    """
    Класс для получения списка датчиков (GET)
    и создания нового датчика (POST).
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorUpdateView(generics.RetrieveUpdateAPIView):
    """
    Класс для получения детальной информации по одному датчику (GET)
    и его обновления (PATCH).
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """
    Класс для добавления нового измерения (POST).
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
