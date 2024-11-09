from rest_framework import viewsets
from reservations.models import Event
from reservations.serializers.event import EventSerializer, EventCreateSerializer
from reservations.utils.paginator import CustomPagination


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "create":
            return EventCreateSerializer
        return EventSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            name = self.request.query_params.get("name")
            category_id = self.request.query_params.get("category_id")
            date_from = self.request.query_params.get("date_from")
            date_to = self.request.query_params.get("date_to")

            if name:
                queryset = queryset.filter(name__icontains=name)

            if category_id:
                queryset = queryset.filter(category_id=category_id)

            if date_from and date_to:
                queryset = queryset.filter(date__range=[date_from, date_to])
            elif date_from:
                queryset = queryset.filter(date__gte=date_from)
            elif date_to:
                queryset = queryset.filter(date__lte=date_to)

        return queryset
