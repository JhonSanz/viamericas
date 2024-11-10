from rest_framework.viewsets import GenericViewSet
from reservations.utils.export_xlsx import export_to_excel
from reservations.serializers.report import ReportSerializer
from reservations.models import Category, Event
from rest_framework.exceptions import ValidationError


class ReportViewSet(GenericViewSet):
    serializer_class = ReportSerializer
    queryset = Category.objects.all()
    authentication_classes = []
    permission_classes = []

    def get_categories_data(self):
        queryset = Category.objects.all()
        return {
            "filename": "categories",
            "headers": ["Nombre", "Descripcion"],
            "model_props": ["name", "description"],
            "Queryset": queryset,
        }

    def get_events_data(self):
        queryset = Event.objects.all()
        return {
            "filename": "categories",
            "headers": ["Nombre", "Descripcion", "Ciudad"],
            "model_props": ["name", "description", "location"],
            "Queryset": queryset,
        }

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        if not serializer.is_valid():
            raise ValidationError("Invalid parameters")

        model_value = serializer.validated_data["model"]

        if model_value == "category":
            data = self.get_categories_data()
        elif model_value == "event":
            data = self.get_events_data()
        else:
            raise ValidationError("Invalid model type")

        return export_to_excel(
            filename=data["filename"],
            headers=data["headers"],
            model_props=data["model_props"],
            Queryset=data["Queryset"],
        )
