import argparse
import requests
from lxml import html
from bs4 import BeautifulSoup
from libgen.models import Keyword


def crawl_libgen(keyword):
    URL = f"https://www.libgen.is/search.php?req={keyword}&open=0&res=25&view=detailed"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    root = html.fromstring(str(soup))
    with open(f"{keyword}.html", "w") as f:
        f.write(html.tostring(root, pretty_print=True).decode())
    books = root.xpath('/html/body/table/font/table')
    print(books)
    for book in books:
        authers = book.xpath('./tbody/tr[3]/td[2]')
        # Get texts from selected elements
        texts = [auther.text_content() for auther in authers]
        # Print the texts
        for text in texts:
            print(text)


if __name__ == "__main__":
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(
        description='Keyword to search in the Libgen site'
    )
    parser.add_argument(
        '--keyword',
        '-k',
        required=True,
        help='Keyword to search in the Libgen site!'
    )
    args = parser.parse_args()

    if args.keyword:
        crawl_libgen(args.keyword)
    else:
        print("No action specified. Use --keyword or -k.")


def perform_database_operations():
    # Your code using Django ORM here
    queryset = Keyword.objects.all()
    for obj in queryset:
        print(f'Title: {obj.title}, Content: {obj.content}')
