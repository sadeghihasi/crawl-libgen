from django.db import models
from manage import init_django
from django.conf import settings


# Initialize the Django environment
init_django()

# Abstract base model providing common fields for other models
class Model(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Marks this model as abstract; won't create a database table for it

# Define specific models inheriting from the abstract base model

class Book(Model):
    # Fields specific to the Book model
    keyword = models.CharField(max_length=50, verbose_name='searched word')
    author_name = models.CharField(max_length=255, verbose_name='author name')
    file_address = models.FileField(
        upload_to=settings.MEDIA_ROOT, max_length=255, verbose_name='download address')
    id = models.CharField(max_length=10, unique=True, verbose_name='id', primary_key=True)
    hash = models.CharField(max_length=32)  # Assuming it's a 32-character hash

    objects = models.Manager()  # Manager for database queries

    def __str__(self):
        # String representation of the Book object
        return f'{self.keyword}'
