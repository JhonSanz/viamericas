from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    FIELD_CHOICES = [
        ("category", "Category"),
        ("event", "Event"),
    ]

    model = serializers.ChoiceField(choices=FIELD_CHOICES)
