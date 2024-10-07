from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Exibe uma mensagem simples no console"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Hello, Django!"))
