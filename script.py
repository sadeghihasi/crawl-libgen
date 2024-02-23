# script.py
from libgen.models import Keyword


word = ""


URL = f"https://www.libgen.is/search.php?req={word}&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"


def perform_database_operations():
    # Your code using Django ORM here
    queryset = Keyword.objects.all()
    for obj in queryset:
        print(f'Title: {obj.title}, Content: {obj.content}')


if __name__ == "__main__":
    perform_database_operations()
