import os
from pathlib import Path
import django
from django.conf import settings
from settings import DATABASES, INSTALLED_APPS


def init_django():

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p1.settings')

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES=DATABASES,
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
    # from django.core.management import call_command
    # call_command('makemigrations', 'libgen')  # Replace with the actual name of your app
