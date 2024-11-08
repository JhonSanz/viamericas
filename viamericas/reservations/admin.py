from django.contrib import admin
from .models import Category, Speaker, Event, Attendee, Reservation

admin.site.register(Category)
admin.site.register(Speaker)
admin.site.register(Attendee)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "location", "category")
    list_filter = ("category", "date")
    search_fields = ("name", "description")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("attendee", "event", "date_reserved", "is_confirmed")
    list_filter = ("is_confirmed", "event")
    search_fields = ("attendee__first_name", "attendee__last_name", "event__name")
