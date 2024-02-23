# your_project/settings.py


# DJANGO SETTINGS
INSTALLED_APPS = ['libgen']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myapp',
        'USER': 'myapp_user',
        'PASSWORD': 'myapp',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
