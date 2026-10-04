from django.db import models


class Sensor(models.Model):
    """Модель датчика."""
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'

    def __str__(self):
        return self.name


class Measurement(models.Model):
    """Модель измерения температуры."""
    # Связь с датчиком. Один датчик может иметь много измерений (One-to-Many).
    # related_name='measurements' критически важно! Оно позволит нам обращаться
    # к списку измерений конкретного датчика при создании сериализатора (по ТЗ).
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements', verbose_name='Датчик')

    # Температура может быть дробной (например, 22.5), поэтому используем FloatField.
    temperature = models.FloatField(verbose_name='Температура')

    # auto_now_add=True автоматически проставит время создания записи (как просили в ТЗ).
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')

    # Поле для картинки (Дополнительное задание).
    # null=True, blank=True делают его необязательным, чтобы старые датчики не сломались.
    image = models.ImageField(upload_to='measurements/', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'

    def __str__(self):
        return f"{self.sensor.name} - {self.temperature}°C"
