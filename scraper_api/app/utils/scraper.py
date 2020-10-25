import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup 
from functools import lru_cache


class InfoMixin:
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
        for tag in self.soup.find_all(cls.TAG, {'class': [cls.CLASS]}):
            res.append(cls(tag))
        return res


class JobPosting(InfoMixin):

    TAG = 'div'
    CLASS = 'jobsearch-SerpJobCard unifiedRow row result'

    def __init__(self, ref):
        self.ref = ref
    
    def __lt__(self, other):
        return self._salary > other._salary

    @property
    @lru_cache(maxsize=None)
    def title(self):
        try: 
            title_text = self.ref.find('a')['title']
        except:
            title_text = ''
        return title_text

    @property
    @lru_cache(maxsize=None)
    def href(self):
        return f"https://www.indeed.com{self.ref.find('a')['href']}"

    @property
    @lru_cache(maxsize=None)
    def salary(self):
        salary_text = self.ref.find('span', {'class': 'salaryText'})
        return salary_text.text.strip() if salary_text != None else ''
    
    @property
    @lru_cache(maxsize=None)
    def _salary(self):
        try: 
            salary = float(self.salary.split(' ')[0][1:])
        except:
            salary = 0
        return salary
    
    @lru_cache(maxsize=None)
    def company(self):
        return self.ref.find('a', {'data-tn-element': 'companyName'}).text.strip()

    @property
    @lru_cache(maxsize=None)
    def info(self):
        '''Returns every attribute labeled with as a property'''
        return super().info()


class CraigslistListing(InfoMixin):

    TAG = 'li'
    CLASS = 'result-row'

    def __init__(self, ref):
        self.ref = ref

    def __repr__(self):
        return f"{self.title}\n{self.href}\n{self.price}\n"

    def __lt__(self, other):
        return (self._price_int * -1, self._time_ts) > (other._price_int * -1, other._time_ts)

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
    def _time_ts(self):
        return datetime.strptime("2020 " + self.time, "%Y %a %d %b %H:%M:%S %p")

    @property
    @lru_cache(maxsize=None)
    def _price_int(self):
        return int(self.price[1:].replace(',',''))

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
    def image_href(self):
        html = requests.get(self.href).text
        scraper = BeautifulSoup(html, 'html.parser')
        image_tag = scraper.findAll('img')
        return None if not image_tag else image_tag[0]['src']
        
    @property
    @lru_cache(maxsize=None)
    def info(self):
        '''Returns every attribute labeled with as a property'''
        return super().info()


class Housing(CraigslistListing): 
    def __init__(self, ref):
        super().__init__(ref)

    def __lt__(self, other):
        return self.price < other.price

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
        '''Returns every attribute labeled with as a property'''
        return super().info()


if __name__ == '__main__':
    url = 'https://www.indeed.com/jobs?q=No+Experience&l=78705'
    html = requests.get(url).text
    scraper = Scraper(html)
    listing_array = scraper.find(JobPosting)
    print(listing_array[0].info)
    '''
    start = time.time()
    url = 'https://austin.craigslist.org/d/apartments-housing-for-rent/search/apa'
    html = requests.get(url).text
    scraper = Scraper(html)
    listing_array = scraper.find(Housing)
    print(listing_array)
    end = time.time()
    print(end - start)
    '''