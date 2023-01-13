# A Python script for the entire project

import configparser
import time

import requests
from bs4 import BeautifulSoup
import sys

# function to measure time taken by a function
def time_taken(func):
    # inner function to measure time taken
    def inner(*args, **kwargs):
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Time taken in {func.__name__}: {end - begin}")

    return inner

# function to extract title and meta description from a webpage
def page_description(url):
    # Extracts the page title and meta description from the specified URL.
    # send request and get response
    response = requests.get(url)

    # parse response
    bs = BeautifulSoup(response.text, 'html.parser')
    meta = bs.find('meta', attrs={'name': 'description'})

    print(f"Title: {bs.title.string}")
    print(f"Meta: {meta['content']}")

# function to extract titles, prices and sort the ads by price from olx
def olx_prices(url):
    res = requests.get(url)

    bs = BeautifulSoup(res.text, 'html.parser')

    titles = bs.find_all('img', class_=['fleft'])
    prices = bs.find_all('p', class_='price')

    parsed_titles = []
    for title in titles:
        parsed_titles.append(title['alt'])

    parsed_prices = []
    for price in prices:
        text = price.getText()
        if text.find('Schimb') >= 0:
            price = 0.0
        else:
            price = price.getText().replace('\n', '') \
                .replace(' ', '') \
                .replace('lei', '') \
                .replace(',', '.')
        parsed_prices.append(float(price))

    ads = []
    for i in range(len(parsed_titles)):
        ads.append({'titlu': parsed_titles[i], 'pret': parsed_prices[i]})

    ads.sort(key=lambda el: el['pret'])
    for ad in ads:
        print(f"Anunt: {ad['titlu']}, pret: {ad['pret']}")

# function to measure time taken by the 'olx_prices' function
@time_taken
def olx_prices_with_time(url):
    return olx_prices(url)


if __name__ == '__main__':
    # Read url from the config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config['DEFAULT']['url']
    # page_description(url)

    url2 = config['DEFAULT']['url2']
    # olx_prices(url2)

    custom_url = f"{config['DEFAULT']['olx_url']}{config['DEFAULT']['search_term'].replace(' ', '-')}/"
    #verify if -log is introduced and proceed accordingly
    noOfArgs = len(sys.argv)
    if noOfArgs > 1:
        if sys.argv[1] == '-log':
            olx_prices_with_time(url)

    else:
        olx_prices(custom_url)
