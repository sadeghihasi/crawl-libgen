import argparse
import requests
from lxml import html
from bs4 import BeautifulSoup
from libgen.models import Book
from django.conf import settings


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

        id = book.xpath('./tbody/tr[8]/td[3]')[0].text_content()

        hash = book.xpath(
            './tbody/tr[11]/td[4]//a/@href')[0].replace("https://library.bz/main/edit/", "")

        download_page_url = f"https://library.lol/main/{hash}"
        response = requests.get(download_page_url)
        if "content-disposition" in response.headers:
            content_disposition = response.headers["content-disposition"]
            file_name = content_disposition.split("filename=")[1]
        else:
            file_name = hash
        file_path = f"{settings.BASE_DIR}/uploads/{file_name}"
        with open(file_path, "w") as f:
            f.write(response.content)

        Book.objects.create(author_name=" ".join(
            texts), keyword=keyword, id=id, file_address=file_path, hash=hash)


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
