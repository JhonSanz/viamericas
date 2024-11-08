# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reservations.views.event import EventViewSet
from reservations.views.reservation import ReservationViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"reservations", ReservationViewSet)

urlpatterns = []
urlpatterns += router.urls
