import argparse
import os
import re
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup
from lxml import html
from retrying import retry

import settings
from db_utilities.create_table import create_table_book
from db_utilities.models import Book  # Assuming the Book model is defined in libgen.models

# Define the output file path for the report
REPORT_OUTPUT_FILE_PATH = 'output.tsv'


# Retry decorator to make a resilient HTTP request
@retry(stop_max_attempt_number=3, wait_fixed=100)
def make_request(url):
    """ Make get request
    """
    response = requests.get(url, timeout=(3, 10))
    response.raise_for_status()
    return response


def extract_downloaded_file_name(content_disposition):
    """
    Extract file name from content_disposition of request header
    """

    # Use regular expression to extract filename
    filename_match = re.search(r'filename=["\'](.*?)["\']', content_disposition)

    if filename_match:
        file_name_encoded = filename_match.group(1)
        file_name = unquote(file_name_encoded)

        return file_name

    # If filename header is not present, fallback to a default name or handle accordingly
    return False


def download_from_cloudflare(book_hash: str) -> str:
    """
    Download book file from cloudflare
    Return downloaded file path
    """

    # Construct the download page URL
    download_page_url = f"https://library.lol/main/{book_hash}"

    # Make a request to the book's download page
    download_page_response = make_request(url=download_page_url)

    soup = BeautifulSoup(download_page_response.text, 'html.parser')
    root = html.fromstring(str(soup))

    # Extract information for each book
    download_link = root.xpath("//tr/td/div/ul/li/a[text()='Cloudflare']/@href")[0]

    response = make_request(url=download_link)

    # Check if the download page is accessible
    if response.status_code == 200:
        file_name = book_hash
        # Determine the file name from the response headers
        if "content-disposition" in response.headers:
            content_disposition = response.headers["content-disposition"]
            extracted_file_name = extract_downloaded_file_name(content_disposition)
            if extracted_file_name:
                file_name = extracted_file_name

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

    return file_path


# Function to crawl Libgen for a given keyword
def crawl_libgen(keyword):
    # Libgen search URL
    url = f"https://www.libgen.is/search.php?req={keyword}&open=0&res=25&view=detailed"

    # Make an HTTP request to the Libgen search page
    response = make_request(url=url)

    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')
    root = html.fromstring(str(soup))

    create_table_book(model=Book)

    # Extract information for each book
    books = root.xpath('/html/body/table/font/table')
    for book in books:
        authors = book.xpath('./tbody/tr[3]/td[2]')
        texts = [author.text_content() for author in authors]
        book_id = book.xpath('./tbody/tr[8]/td[4]')[0].text_content()
        hash_value = book.xpath('./tbody/tr[11]/td[4]//a/@href')[0].replace("https://library.bz/main/edit/", "")

        file_path = download_from_cloudflare(book_hash=hash_value)

        # Create or update a Book object in the database
        Book.get_or_create(author_name=" ".join(texts), keyword=keyword, id=book_id, file_address=file_path,
                           hash=hash_value)


# Function to generate a report for a given keyword
def report_libgen(keyword):
    # Retrieve Book objects from the database based on the keyword
    results = Book.filter(keyword=keyword)

    # Get the field names of the Book model
    field_names = ["keyword", "author_name", "file_address", "id", "hash"]  # TODO

    # Write the header with column names to the file
    with open(REPORT_OUTPUT_FILE_PATH, 'w') as file:
        file.write('\t'.join(field_names) + '\n')

        # Iterate through the queryset and write values to the file
        for row in results:
            values = [str(getattr(row, field)) for field in field_names]
            file.write('\t'.join(values) + '\n')

    print(f"Reports written to {REPORT_OUTPUT_FILE_PATH}")


# Main block to handle command-line arguments
if __name__ == "__main__":
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Keyword to search and report in the Libgen site')
    parser.add_argument('--keyword', '-k', required=False, help='Keyword to search in the Libgen site!')
    parser.add_argument('--report', '-r', required=False, help='Keyword to get the report!')
    args = parser.parse_args()

    # Perform actions based on command-line arguments
    if args.keyword:
        crawl_libgen(args.keyword)
    elif args.report:
        report_libgen(args.report)
    else:
        print(
            "No action specified.\n\t"
            "Use --keyword or -k to search and store data.\n\t"
            "Use --report or -r to get the report.")
