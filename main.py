import argparse
import os

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from lxml import html
from retrying import retry

from libgen.models import Book


@retry(stop_max_attempt_number=3, wait_fixed=100)
def make_request(url):
    response = requests.get(url, timeout=(3, 10))
    response.raise_for_status()
    return response


def crawl_libgen(keyword):
    URL = f"https://www.libgen.is/search.php?req={keyword}&open=0&res=25&view=detailed"
    response = make_request(url=URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    root = html.fromstring(str(soup))
    with open(f"{keyword}.html", "w") as f:
        f.write(html.tostring(root, pretty_print=True).decode())
    books = root.xpath('/html/body/table/font/table')
    for book in books:
        authers = book.xpath('./tbody/tr[3]/td[2]')
        # Get texts from selected elements
        texts = [auther.text_content() for auther in authers]
        # Print the texts

        id = book.xpath('./tbody/tr[8]/td[4]')[0].text_content()

        hash = book.xpath('./tbody/tr[11]/td[4]//a/@href')[0].replace("https://library.bz/main/edit/", "")

        download_page_url = f"https://library.lol/main/{hash}"
        response = make_request(url=download_page_url)
        if response.status_code == 200:
            if "content-disposition" in response.headers:
                content_disposition = response.headers["content-disposition"]
                file_name = content_disposition.split("filename=")[1]
            else:
                file_name = hash

            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            # Create a directory if it doesn't exist.
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            print("The book download page is not available!")
            file_path = None

        Book.objects.get_or_create(author_name=" ".join(texts), keyword=keyword, id=id, file_address=file_path,
                                   hash=hash)


def report_libgen(keyword):
    results = Book.objects.filter(kwargs=keyword)
    for row in results:
        # Access each row's attributes as needed
        print(row)
    
    OUTPUT_FILE_PATH = 'output.csv'
    field_names = [field.name for field in Book._meta.get_fields()]
    with open(OUTPUT_FILE_PATH, 'w') as file:
        # Write the header with column names to the file
        file.write(','.join(field_names) + '\n')

        # Iterate through the queryset
        for row in results:
            # Write the values of all columns to the file
            values = [str(getattr(row, field)) for field in field_names]
            file.write(','.join(values) + '\n')
    print(f"Reports written to {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Keyword to search and report in the Libgen site')
    parser.add_argument('--keyword', '-k', required=True, help='Keyword to search in the Libgen site!')
    parser.add_argument('--report', '-r', required=False, help='Keyword to get the report!')
    args = parser.parse_args()

    if args.keyword:
        crawl_libgen(args.keyword)
    elif args.report:
        report_libgen(args.report)
    else:
        print("No action specified.\n\tUse --keyword or -k to search and store data.\n\tUse --report or -r to get the report.")
