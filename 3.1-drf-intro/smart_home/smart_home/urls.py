from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем все маршруты из нашего приложения measurement
    # Все они будут доступны с приставкой /api/ (например, /api/sensors/)
    path('api/', include('measurement.urls')),
]
