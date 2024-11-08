from rest_framework import viewsets
from reservations.models import Event
from reservations.views import EventSerializer, EventCreateSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return EventCreateSerializer
        return EventSerializer
