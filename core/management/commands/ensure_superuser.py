import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Command(BaseCommand):
    help = "Create a superuser from environment variables if one does not already exist."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        reset_password = env_bool("DJANGO_SUPERUSER_RESET_PASSWORD", default=False)

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping superuser creation: set DJANGO_SUPERUSER_USERNAME and "
                    "DJANGO_SUPERUSER_PASSWORD to enable it."
                )
            )
            return

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        fields_changed = False

        if created:
            user.set_password(password)
            fields_changed = True
        elif reset_password:
            user.set_password(password)
            fields_changed = True

        if email and user.email != email:
            user.email = email
            fields_changed = True

        if not user.is_staff:
            user.is_staff = True
            fields_changed = True

        if not user.is_superuser:
            user.is_superuser = True
            fields_changed = True

        if fields_changed:
            user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
        elif reset_password:
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' already existed; details synchronized.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' already exists; no changes needed.")
            )
