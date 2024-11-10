from django.contrib import admin
from .models import Category, Speaker, Event, Attendee, Reservation
from .models import Event
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.utils import timezone
from .models import Event
import datetime


class CustomAdminSite(admin.AdminSite):
    site_header = "Viamericas Admin"

    def index(self, request, extra_context=None):
        today = timezone.now().date()
        next_week = today + datetime.timedelta(days=7)
        upcoming_events = Event.objects.filter(date__range=(today, next_week))

        if extra_context is None:
            extra_context = {}
        extra_context["upcoming_events"] = upcoming_events

        return super().index(request, extra_context=extra_context)


admin_site = CustomAdminSite(name="custom_admin")


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("attendee", "event", "date_reserved", "is_confirmed")
    list_filter = ("is_confirmed", "event")
    search_fields = ("attendee__first_name", "attendee__last_name", "event__name")


class EventDateFilter(admin.SimpleListFilter):
    title = "Event date"
    parameter_name = "event_date"

    def lookups(self, request, model_admin):
        return (
            ("today", "Today"),
            ("past_week", "Past 7 days"),
            ("this_month", "This month"),
            ("this_year", "This year"),
        )

    def queryset(self, request, queryset):
        from django.utils import timezone
        import datetime

        today = timezone.now().date()

        if self.value() == "today":
            return queryset.filter(date__date=today)
        elif self.value() == "past_week":
            last_week = today - datetime.timedelta(days=7)
            return queryset.filter(date__date__gte=last_week)
        elif self.value() == "this_month":
            return queryset.filter(date__month=today.month, date__year=today.year)
        elif self.value() == "this_year":
            return queryset.filter(date__year=today.year)
        return queryset


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "location", "category")
    search_fields = ["name", "location", "category__name"]
    list_filter = (EventDateFilter,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        date = request.GET.get("date")
        if date:
            qs = qs.filter(date__date=date)
        return qs


admin_site.register(User)
admin_site.register(Group)
admin_site.register(Event, EventAdmin)
admin_site.register(Reservation, ReservationAdmin)
admin_site.register(Category)
admin_site.register(Speaker)
admin_site.register(Attendee)
