from rest_framework import serializers
from reservations.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ("id",)


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "location", "category", "speakers"]
