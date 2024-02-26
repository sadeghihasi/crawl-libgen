import argparse
import os

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from lxml import html
from retrying import retry

from libgen.models import Book  # Assuming the Book model is defined in libgen.models

# Retry decorator to make a resilient HTTP request
@retry(stop_max_attempt_number=3, wait_fixed=100)
def make_request(url):
    response = requests.get(url, timeout=(3, 10))
    response.raise_for_status()
    return response

# Function to crawl Libgen for a given keyword
def crawl_libgen(keyword):
    # Libgen search URL
    URL = f"https://www.libgen.is/search.php?req={keyword}&open=0&res=25&view=detailed"

    # Make an HTTP request to the Libgen search page
    response = make_request(url=URL)

    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    root = html.fromstring(str(soup))

    # Save the HTML for debugging purposes
    with open(f"{keyword}.html", "w") as f:
        f.write(html.tostring(root, pretty_print=True).decode())

    # Extract information for each book
    books = root.xpath('/html/body/table/font/table')
    for book in books:
        authors = book.xpath('./tbody/tr[3]/td[2]')
        texts = [author.text_content() for author in authors]
        book_id = book.xpath('./tbody/tr[8]/td[4]')[0].text_content()
        hash_value = book.xpath('./tbody/tr[11]/td[4]//a/@href')[0].replace("https://library.bz/main/edit/", "")

        # Construct the download page URL
        download_page_url = f"https://library.lol/main/{hash_value}"

        # Make a request to the book's download page
        response = make_request(url=download_page_url)

        # Check if the download page is accessible
        if response.status_code == 200:
            # Determine the file name from the response headers
            if "content-disposition" in response.headers:
                content_disposition = response.headers["content-disposition"]
                file_name = content_disposition.split("filename=")[1]
            else:
                file_name = hash_value

            # Define the file path
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            # Create a directory if it doesn't exist
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)

            # Save the file content
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            print("The book download page is not available!")
            file_path = None

        # Create or update a Book object in the database
        Book.objects.get_or_create(author_name=" ".join(texts), keyword=keyword, id=book_id,
                                   file_address=file_path, hash=hash_value)

# Function to generate a report for a given keyword
def report_libgen(keyword):
    # Retrieve Book objects from the database based on the keyword
    results = Book.objects.filter(keyword=keyword)

    # Print information for each Book
    for row in results:
        # Access each row's attributes as needed
        print(row)

    # Define the output file path for the report
    OUTPUT_FILE_PATH = 'output.csv'

    # Get the field names of the Book model
    field_names = [field.name for field in Book._meta.get_fields()]

    # Write the header with column names to the file
    with open(OUTPUT_FILE_PATH, 'w') as file:
        file.write(','.join(field_names) + '\n')

        # Iterate through the queryset and write values to the file
        for row in results:
            values = [str(getattr(row, field)) for field in field_names]
            file.write(','.join(values) + '\n')

    print(f"Reports written to {OUTPUT_FILE_PATH}")

# Main block to handle command-line arguments
if __name__ == "__main__":
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Keyword to search and report in the Libgen site')
    parser.add_argument('--keyword', '-k', required=True, help='Keyword to search in the Libgen site!')
    parser.add_argument('--report', '-r', required=False, help='Keyword to get the report!')
    args = parser.parse_args()

    # Perform actions based on command-line arguments
    if args.keyword:
        crawl_libgen(args.keyword)
    elif args.report:
        report_libgen(args.report)
    else:
        print("No action specified.\n\tUse --keyword or -k to search and store data.\n\tUse --report or -r to get the report.")
