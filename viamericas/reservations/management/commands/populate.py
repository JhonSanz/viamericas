# miapp/management/commands/mi_comando.py

from django.core.management.base import BaseCommand
from reservations.seed import DataCreator


class Command(BaseCommand):
    help = "Este comando crea la información necesaria para que esto funcione"

    def handle(self, *args, **options):
        DataCreator().run()
        self.stdout.write("Created everything :)")
