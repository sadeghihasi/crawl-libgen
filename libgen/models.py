# db/models.py
from django.db import models
from manage import init_django
from django.conf import settings


init_django()


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# define models here


class Book(Model):
    keyword = models.CharField(max_length=50, verbose_name='searched word')
    author_name = models.CharField(max_length=255, verbose_name='auther name')
    file_address = models.FileField(
        upload_to=f'{settings.BASE_DIR}/uploads/', verbose_name='downloal address')
    file = models.FileField()  # Set your desired upload path

    id = models.CharField(max_length=10, unique=True, verbose_name='id', primary_key=True)
    hash = models.CharField(max_length=32)  # Assuming it's a 32-character hash

    objects = models.Manager()

    def __str__(self):
        return f'{self.keyword}'
