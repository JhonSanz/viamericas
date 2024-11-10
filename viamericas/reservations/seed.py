from reservations.models import (
    Attendee,
    Speaker,
    Reservation,
    Event,
    Category,
)
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission


class DataCreator:
    def __init__(self):
        self.users = []
        self.categories = []
        self.speakers = []
        self.attendees = []
        self.events = []

    def run(self):
        self.create_users()
        self.create_categories()
        self.create_speakers()
        self.create_attendees()
        self.create_events()
        self.create_reservations()

    def create_users(self):
        superuser = User.objects.create(
            username="viamericas",
            email="viamericas@example.com",
            password=make_password("holamundo123"),
            is_superuser=True,
            is_staff=True,
        )

        models_with_permissions = [
            Category,
            Speaker,
            Event,
            Attendee,
            Reservation,
        ]
        for model_name in models_with_permissions:
            model_content_type = ContentType.objects.get_for_model(model_name)
            permissions = Permission.objects.filter(content_type=model_content_type)
            superuser.user_permissions.add(*permissions)

        restricted_user = User.objects.create(
            username="restricted_user",
            email="restricted@example.com",
            password=make_password("restrictedpass123"),
            is_superuser=False,
            is_staff=True,
        )

        ct_reservation = ContentType.objects.get_for_model(Reservation)
        ct_event = ContentType.objects.get_for_model(Event)

        restricted_permissions = [
            Permission.objects.get(
                codename="view_reservation",
                content_type=ct_reservation,
            ),
            Permission.objects.get(
                codename="change_reservation",
                content_type=ct_reservation,
            ),
            Permission.objects.get(
                codename="view_event",
                content_type=ct_event,
            ),
        ]
        restricted_user.user_permissions.add(*restricted_permissions)
        self.users = [superuser, restricted_user]

    def create_categories(self):
        data = [
            {
                "name": "Conferencia",
                "description": "Categoría para conferencias generales.",
            },
            {
                "name": "Capacitación",
                "description": "Categoría para capacitaciones.",
            },
            {
                "name": "Clase magistral",
                "description": "Categoría para clases magistrales.",
            },
        ]

        for category_data in data:
            category_created, _ = Category.objects.get_or_create(**category_data)
            self.categories.append(category_created)

    def create_speakers(self):
        speakers = [
            {
                "first_name": "Albert",
                "last_name": "Einstein",
                "email": "einstein@example.com",
                "bio": "Físico teórico, conocido por la teoría de la relatividad.",
            },
            {
                "first_name": "Marie",
                "last_name": "Curie",
                "email": "curie@example.com",
                "bio": "Científica polaca-francesa, pionera en el campo de la radiactividad.",
            },
            {
                "first_name": "Nikola",
                "last_name": "Tesla",
                "email": "tesla@example.com",
                "bio": "Inventor, ingeniero eléctrico y mecánico, conocido por sus contribuciones al desarrollo de sistemas eléctricos de corriente alterna.",
            },
        ]

        for speaker_data in speakers:
            speaker_created, _ = Speaker.objects.get_or_create(**speaker_data)
            self.speakers.append(speaker_created)

    def create_attendees(self):
        attendees = [
            {"first_name": "John", "last_name": "Doe", "email": "johndoe@example.com"},
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "janesmith@example.com",
            },
            {
                "first_name": "Alice",
                "last_name": "Johnson",
                "email": "alicejohnson@example.com",
            },
            {
                "first_name": "Bob",
                "last_name": "Brown",
                "email": "bobbrown@example.com",
            },
        ]

        for attendee_data in attendees:
            attendee_created, _ = Attendee.objects.get_or_create(**attendee_data)
            self.attendees.append(attendee_created)

    def create_events(self):
        events = [
            {
                "name": "Clase de quimica",
                "description": "Quimica avanzada universidad nacional",
                "date": "2024-11-10",
                "location": "Dosquebradas",
                "category": self.categories[0],
                "speakers": [self.speakers[0]],
            },
            {
                "name": "Mecánica cuántica para todos",
                "description": "Conferencia sobre mecánica cuántica de la nueva era",
                "date": "2024-11-10",
                "location": "Pereira",
                "category": self.categories[1],
                "speakers": [self.speakers[1]],
            },
        ]

        for event_data in events:
            speaker = event_data.pop("speakers")
            e, _ = Event.objects.get_or_create(**event_data)
            e.speakers.set(speaker)
            self.events.append(e)

    def create_reservations(self):
        reservations = [
            {
                "attendee": self.attendees[0],
                "event": self.events[0],
                "date_reserved": "2024-11-10",
                "is_confirmed": False,
            },
            {
                "attendee": self.attendees[1],
                "event": self.events[1],
                "date_reserved": "2024-11-10",
                "is_confirmed": True,
            },
        ]

        for reservation_data in reservations:
            Reservation.objects.get_or_create(**reservation_data)
