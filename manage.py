import os
from pathlib import Path

import django
from django.conf import settings

from settings import DATABASES, INSTALLED_APPS


def init_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p1.settings')

    if settings.configured:
        return

    base_dir = Path(__file__).resolve().parent

    settings.configure(INSTALLED_APPS=INSTALLED_APPS, DATABASES=DATABASES,
                       # Build paths inside the project like this: BASE_DIR / 'subdir'.
                       BASE_DIR=base_dir, MEDIA_ROOT=os.path.join(base_dir, "uploads"))
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
