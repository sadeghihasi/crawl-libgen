from settings import DATABASES, INSTALLED_APPS


def init_django():
    import os
    import django
    from django.conf import settings


    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p1.settings')

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES=DATABASES
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
