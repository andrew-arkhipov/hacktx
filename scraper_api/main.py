from bs4 import BeautifulSoup 
import requests
import time
import concurrent.futures
from functools import cached_property

class Listing: 
    def __init__(self, ref):
        self.ref = ref

    def __repr__(self):
        return f"{self.title}\n{self.href}\n{self.price}"

    @cached_property
    def title(self):
        return self.ref.find('a', {'class':['result-title hdrlnk']}, href=True).text

    @cached_property
    def href(self):
        return self.ref.find('a', {'class':['result-title hdrlnk']}, href=True)['href']

    @cached_property
    def time(self):
        return self.ref.find('time', {'class':['result-date']})['title']

    @cached_property
    def price(self):
        return self.ref.find('span', {'class':['result-price']}).text

    @cached_property
    def body(self):
        html = requests.get(self.href).text
        scraper = BeautifulSoup(html, 'html.parser')
        body = scraper.find('section', {'id':['postingbody']})
        return body.text

    @cached_property
    def info(self):
        return self.title, self.href, self.price, self.time


class Scraper:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def find_listings(self):
        res = []
        for tag in self.soup.findAll('li', {'class':['result-row']}):
            res.append(Listing(tag))
        return res


def main(url):
    html = requests.get(url).text
    scraper = Scraper(html)
    info = scraper.find_listings()
    print(info)


if __name__ == '__main__':
    start = time.time()
    url = 'https://austin.craigslist.org/search/fua?query=bed'
    html = requests.get(url).text
    scraper = Scraper(html)
    listing_array = scraper.find_listings()

    bodies = []
    for listing in listing_array: 
        bodies.append(listing.body)
        
    end = time.time()
    print(end - start)