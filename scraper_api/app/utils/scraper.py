import requests
import time
from datetime import datetime
import concurrent.futures
from bs4 import BeautifulSoup 
from functools import lru_cache


class InfoMixin:
    @property
    def info(self):
        res = {}
        for k in dir(self):
            try:
                attr = getattr(self.__class__, k)
            except:
                continue
            if isinstance(attr, property) and k not in {'body', 'info'}:
                res[k] = attr.fget(self)
        return res


class Scraper:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def find(self, cls):
        res = []
        for tag in self.soup.findAll(cls.TAG, {'class': [cls.CLASS]}):
            res.append(cls(tag))
        return res


class JobPosting:

    TAG = 'div'
    CLASS = 'jobsearch-SerpJobCard unifiedRow row result clickcard'

    def __init__(self, ref):
        self.ref = ref


class CraigslistListing(InfoMixin):

    TAG = 'li'
    CLASS = 'result-row'

    def __init__(self, ref):
        self.ref = ref

    def __repr__(self):
        return f"{self.title}\n{self.href}\n{self.price}"

    def __lt__(self, other):
        return (self.price_int * -1, self.time_ts) > (other.price_int * -1, other.time_ts)

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
    def time_ts(self):
        return datetime.strptime("2020 " + self.time, "%Y %a %d %b %H:%M:%S %p")

    @property
    @lru_cache(maxsize=None)
    def time_ts(self):
        return datetime.strptime("2020 " + self.time, "%Y %a %d %b %H:%M:%S %p")

    @property
    @lru_cache(maxsize=None)
    def price_int(self):
        return int(self.price[1:].replace(',',''))

    @property
    @lru_cache(maxsize=None)
    def price(self):
        return self.ref.find('span', {'class':['result-price']}).text

    @property
    @lru_cache(maxsize=None)
    def price_int(self):
        return int(self.price[1:].replace(',',''))

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
        return super().info


class Housing(CraigslistListing): 
    def __init__(self, ref):
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
        return super().info


if __name__ == '__main__':  
    start = time.time()
    url = 'https://austin.craigslist.org/d/apartments-housing-for-rent/search/apa'
    html = requests.get(url).text
    scraper = CraigslistScraper(html)
    listing_array = scraper.find(Housing)
    print(listing_array)
    end = time.time()
    print(end - start)