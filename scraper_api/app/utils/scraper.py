import requests
import time
import concurrent.futures
from bs4 import BeautifulSoup 
from functools import lru_cache

class Listing: 
    def __init__(self, ref):
        self.ref = ref

    def __repr__(self):
        return f"{self.title}\n{self.href}\n{self.price}"

    @classmethod
    def create_listing(cls, ref):
        return cls(ref)

    @property
    @lru_cache
    def title(self):
        return self.ref.find('a', {'class':['result-title hdrlnk']}, href=True).text

    @property
    @lru_cache
    def href(self):
        return self.ref.find('a', {'class':['result-title hdrlnk']}, href=True)['href']

    @property
    @lru_cache
    def time(self):
        return self.ref.find('time', {'class':['result-date']})['title']

    @property
    @lru_cache
    def price(self):
        return self.ref.find('span', {'class':['result-price']}).text

    @property
    @lru_cache
    def body(self):
        html = requests.get(self.href).text
        scraper = BeautifulSoup(html, 'html.parser')
        body = scraper.find('section', {'id':['postingbody']})
        return body.text

    @property
    @lru_cache
    def info(self):
        return self.title, self.href, self.price, self.time


class Scraper:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def find_listings(self):
        res = list(map(Listing.create_listing, self.soup.findAll('li', {'class': ['result-row']})))
        return res


def get_body(listing):
    return listing.body


if __name__ == '__main__':
    start = time.time()
    url = 'https://austin.craigslist.org/search/fua?query=bed'
    html = requests.get(url).text
    scraper = Scraper(html)
    listing_array = scraper.find_listings()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        bodies = list(executor.map(get_body, listing_array))
        
    end = time.time()
    print(end - start)