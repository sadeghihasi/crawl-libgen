# db/models.py
from django.db import models
from manage import init_django

init_django()


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# define models here


class Keyword(Model):
    keyword = models.CharField(max_length=50, verbose_name='searched word')
    author_name = models.CharField(max_length=255, verbose_name='auther name')
    download_address = models.URLField(verbose_name='downloal address')
    ids = models.CharField(max_length=10, unique=True, verbose_name='ids')

    objects = models.Manager()

    def __str__(self):
        return f'{self.keyword}'
