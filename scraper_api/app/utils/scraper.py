import requests
import time
import datetime
import concurrent.futures
from bs4 import BeautifulSoup 
from functools import lru_cache


class CraigslistListing: 
    def __init__(self, ref):
        self.ref = ref

    def __repr__(self):
        return f"{self.title}\n{self.href}\n{self.price}"

    def __lt__(self, other):
        get_price = lambda p: int(p[1:].replace(',','')) * -1
        get_date = lambda d: datetime.strptime("2020 " + d, "%Y %a %d %b %H:%M:%S %p")
        return (get_price(self.price), get_date(self.time)) > (get_price(other.price), get_date(other.time))

    @property
    @lru_cache(maxsize=None)
    def title(self):
        return self.ref.find('a', {'class':['result-title hdrlnk']}, href=True).text

    @property
    @lru_cache(maxsize=None)
    def href(self):
        return self.ref.find('a', {'class':['result-title hdrlnk']}, href=True)['href']

    @property
    @lru_cache(maxsize=None)
    def time(self):
        return self.ref.find('time', {'class':['result-date']})['title']

    @property
    @lru_cache(maxsize=None)
    def price(self):
        return self.ref.find('span', {'class':['result-price']}).text

    @property
    @lru_cache(maxsize=None)
    def body(self):
        html = requests.get(self.href).text
        scraper = BeautifulSoup(html, 'html.parser')
        body = scraper.find('section', {'id':['postingbody']})
        return body.text

    @property
    @lru_cache(maxsize=None)
    def info(self):
        return self.title, self.href, self.price, self.time

class Housing(CraigslistListing): 
    def __init__(self, ref):
        self.ref = ref 
        super().__init__(ref)

    def __repr__(self):
        return f"{self.title}\n{self.href}\n{self.price}\n{self.square_foot}"
    
    @property
    @lru_cache(maxsize=None)
    def square_foot(self):
        main_tag = self.ref.find('span', {'class':['result-meta']})
        res = self.ref.find('span', {'class':['housing']})
        return None if not res else res.text.lstrip().rstrip()

    @property
    @lru_cache(maxsize=None)
    def info(self):
        return self.title, self.href, self.price, self.time, self.square_foot


class Scraper:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')


class CraigslistScraper(Scraper):
    def __init__(self, html):
        super().__init__(html)

    def find(self, cls):
        res = []
        for tag in self.soup.findAll('li', {'class': ['result-row']}):
            res.append(cls(tag))
        return res


class IndeedScraper(Scraper):
    def __init__(self, html):
        super().__init__(html)


if __name__ == '__main__':
    start = time.time()
    url = 'https://austin.craigslist.org/d/apartments-housing-for-rent/search/apa'
    html = requests.get(url).text
    scraper = Scraper(html)
    listing_array = scraper.find_type(Housing)
    print(listing_array)
    end = time.time()
    print(end - start)