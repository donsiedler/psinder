from django.core.management.base import BaseCommand
from ._private import create_fake_user


class Command(BaseCommand):
    help = "Populates the database with fake users"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, default=10,
                            help="an integer for the amount of profiles to generate")

    def handle(self, *args, **options):
        profiles_to_generate = options["count"]
        if profiles_to_generate:
            for _ in range(profiles_to_generate):
                create_fake_user()
            self.stdout.write(self.style.SUCCESS(f"Successfully populated with {profiles_to_generate} users"))
        else:
            create_fake_user()
            self.stdout.write(self.style.SUCCESS("Successfully populated with 1 user"))
