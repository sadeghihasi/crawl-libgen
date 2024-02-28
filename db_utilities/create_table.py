from db_utilities.database_manager import DatabaseManager
from settings import DATABASE


def create_table_book(model):
    database_manager = DatabaseManager(
        database_name=DATABASE['NAME'],
        user=DATABASE['USER'],
        password=DATABASE['PASSWORD'],
        host=DATABASE['HOST'],
        port=DATABASE['PORT'],
    )

    database_manager.create_tables(models=[model])
