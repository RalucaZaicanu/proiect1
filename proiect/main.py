# A Python script for extracting the page title and meta description from a URL.

import configparser
import requests
from bs4 import BeautifulSoup


def page_description(url):
    # Extracts the page title and meta description from the specified URL.
    # send request and get response
    response = requests.get(url)

    # parse response
    bs = BeautifulSoup(response.text, 'html.parser')
    meta = bs.find('meta', attrs={'name': 'description'})

    print(f"Title: {bs.title.string}")
    print(f"Meta: {meta['content']}")


if __name__ == '__main__':
    # Read url from the config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config['DEFAULT']['url']

    # Extract the page info
    page_description(url)