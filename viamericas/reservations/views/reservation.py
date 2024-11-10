from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from reservations.models import Reservation
from reservations.serializers.reservation import (
    ReservationSerializer,
    ReservationCreateSerializer,
)
from reservations.utils.paginator import CustomPagination


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            attendee_name = self.request.query_params.get("attendee_name")
            event_id = self.request.query_params.get("event_id")
            date_reserved_from = self.request.query_params.get("date_reserved_from")
            date_reserved_to = self.request.query_params.get("date_reserved_to")
            is_confirmed = self.request.query_params.get("is_confirmed")

            if attendee_name:
                queryset = queryset.filter(attendee__name__icontains=attendee_name)

            if event_id:
                queryset = queryset.filter(event_id=event_id)

            if date_reserved_from and date_reserved_to:
                queryset = queryset.filter(
                    date_reserved__range=[date_reserved_from, date_reserved_to]
                )
            elif date_reserved_from:
                queryset = queryset.filter(date_reserved__gte=date_reserved_from)
            elif date_reserved_to:
                queryset = queryset.filter(date_reserved__lte=date_reserved_to)

            if is_confirmed:
                queryset = queryset.filter(is_confirmed=is_confirmed)

        return queryset
