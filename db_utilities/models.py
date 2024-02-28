import peewee

from db_utilities.database_manager import DatabaseManager
from settings import DATABASE

database_manager = DatabaseManager(
    database_name=DATABASE['NAME'],
    user=DATABASE['USER'],
    password=DATABASE['PASSWORD'],
    host=DATABASE['HOST'],
    port=DATABASE['PORT'],
)


class Book(peewee.Model):
    # Fields specific to the Book model
    keyword = peewee.CharField(max_length=500, verbose_name='searched word')
    author_name = peewee.CharField(max_length=500, verbose_name='author name')
    file_address = peewee.CharField(max_length=500, verbose_name='download address')
    id = peewee.CharField(max_length=10, unique=True, verbose_name='id', primary_key=True)
    hash = peewee.CharField(max_length=32)  # Assuming it's a 32-character hash

    class Meta:
        database = database_manager.db

    def __str__(self):
        # String representation of the Book object
        return f'{self.keyword}'
