# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reservations.views.event import EventViewSet
from reservations.views.reservation import ReservationViewSet
from reservations.views.report import ReportViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"reservations", ReservationViewSet)
router.register(r"report", ReportViewSet)

urlpatterns = []
urlpatterns += router.urls
