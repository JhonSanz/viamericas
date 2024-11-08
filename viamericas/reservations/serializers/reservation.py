from rest_framework import serializers
from reservations.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    attendee_name = serializers.CharField(source="attendee.first_name", read_only=True)
    event_name = serializers.CharField(source="event.name", read_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ("id", "date_reserved")


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["attendee", "event", "is_confirmed"]
