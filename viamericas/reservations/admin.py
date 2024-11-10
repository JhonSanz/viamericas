from django.contrib import admin
from django.utils import timezone
import datetime
from .models import Category, Speaker, Event, Attendee, Reservation
from .models import Event
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.utils import timezone
from .models import Event
import datetime
from django.db.models import Count, F
from django.db.models.functions import Upper
from io import BytesIO
from django.utils.safestring import mark_safe
import base64
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class CustomAdminSite(admin.AdminSite):
    site_header = "Viamericas Admin"

    def __generate_chart(self, *, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        events_by_category = Event.objects.values("category__name").annotate(
            total=Count("id")
        )

        labels = [entry["category__name"] for entry in events_by_category]
        sizes = [entry["total"] for entry in events_by_category]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode("utf-8")

        extra_context["events_pie_chart"] = mark_safe(
            f'<img src="data:image/png;base64,{graphic}" />'
        )

        return super().index(request, extra_context=extra_context)

    def index(self, request, extra_context=None):
        today = timezone.now().date()
        next_week = today + datetime.timedelta(days=7)
        upcoming_events = Event.objects.filter(date__range=(today, next_week))

        if extra_context is None:
            extra_context = {}
        extra_context["upcoming_events"] = upcoming_events

        self.__generate_chart(request=request, extra_context=extra_context)

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
    list_display = ("name", "date", "location", "category", "total_reservations")
    search_fields = ["name", "location", "category__name"]
    list_filter = (EventDateFilter,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        date = request.GET.get("date")
        if date:
            qs = qs.filter(date__date=date)
        return qs

    def total_reservations(self, obj):
        return obj.reservations.count()

    total_reservations.short_description = "Total Reservations"

    @admin.action(description="Convertir nombres a mayúsculas")
    def make_uppercase(self, request, queryset):
        queryset.update(name=Upper(F("name")))

    @admin.action(description="Capitalizar nombres")
    def make_capitalize(self, request, queryset):
        for event in queryset:
            event.name = event.name.title()
            event.save()

    actions = ["make_uppercase", "make_capitalize"]


admin_site.register(User)
admin_site.register(Group)
admin_site.register(Event, EventAdmin)
admin_site.register(Reservation, ReservationAdmin)
admin_site.register(Category)
admin_site.register(Speaker)
admin_site.register(Attendee)
