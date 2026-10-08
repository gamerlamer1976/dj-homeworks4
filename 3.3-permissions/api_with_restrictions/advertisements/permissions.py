from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение:
    - Чтение разрешено всем (SAFE_METHODS).
    - Изменение и удаление разрешено только создателю объявления или администратору.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для небезопасных методов (PATCH, PUT, DELETE) проверяем авторство или права админа
        return obj.creator == request.user or request.user.is_staff
