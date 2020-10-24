from bs4 import BeautifulSoup 
import requests
import time

class Listing: 

    def __init__(self, title, href, price, time):
        self.title = title 
        self.href = href
        self.price = price
        self.time = time

    def __repr__(self):
        return self.title + '\n' + self.href + '\n' + self.price

class Scraper:

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def find_listings(self):
        res = []
        for listing in self.soup.findAll('li', {'class':['result-row']}):
            title, href, price, time = self.get_listing_info(listing)
            res.append(Listing(title, href, price, time))
        return res

    def get_listing_info(self, listing):
        title = listing.find('a', {'class':['result-title hdrlnk']}, href=True)
        title_text = title.text
        post_href = title['href']
        time = listing.find('time', {'class':['result-date']})['title']
        price = listing.find('span', {'class':['result-price']}).text
    
        return title_text, post_href, price, time

    def get_listing_body(self):
        body = self.soup.find('section', {'id':['postingbody']})
        return body.text


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

    body = []

    for listing in listing_array: 
        url = listing.href
        html = requests.get(url).text
        scraper = Scraper(html)
        body.append(scraper.get_listing_body())
        
    end = time.time()
    print(end - start)
        
    