from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsOwnerOrReadOnly


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # Указываем базовый queryset
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    # Подключаем фильтр по датам и статусу
    filterset_class = AdvertisementFilter

    # Троттлинг
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        """
        Переопределяем queryset для скрытия черновиков.
        """
        # Базовый кверисет - все объявления, кроме черновиков
        queryset = Advertisement.objects.exclude(status=AdvertisementStatusChoices.DRAFT)

        # Если пользователь авторизован, добавляем к выборке ЕГО черновики
        if self.request.user.is_authenticated:
            user_drafts = Advertisement.objects.filter(
                creator=self.request.user,
                status=AdvertisementStatusChoices.DRAFT
            )
            # Объединяем кверисеты (все не-черновики + черновики текущего юзера)
            queryset = queryset | user_drafts

        return queryset

    def get_permissions(self):
        """Получение прав для действий."""

        # Для создания достаточно быть просто авторизованным
        if self.action == "create":
            return [IsAuthenticated()]

        # Для изменения и удаления нужно быть авторизованным И владельцем (или админом)
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]

        # Для просмотра (list, retrieve) - доступ открыт всем
        return []
