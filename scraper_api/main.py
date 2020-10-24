from bs4 import BeautifulSoup 
import requests

class Furniture: 

    def __init__(self, title, href, price):
        self.title = title 
        self.href = href
        self.price = price

    def __repr__(self):
        return self.title + '\n' + self.href + '\n' + self.price

class Scraper:

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def test(self):
        print(self.soup.prettify())

    def find_listings(self):
        res = []
        for listing in self.soup.findAll('li', {'class':['result-row']}):
            title, href, price = self.get_listing_info(listing)
            res.append(Furniture(title, href, price))
        return res

    def get_listing_info(self, listing):
        title = listing.find('a', {'class':['result-title hdrlnk']}, href=True)
        title_text = title.text
        post_href = title['href']
        time = listing.find('time', {'class':['result-date']})['title']
        price = listing.find('span', {'class':['result-price']}).text
    
        return title_text, post_href, price

def main(url):
    html = requests.get(url).text
    scraper = Scraper(html)
    info = scraper.find_listings()
    print(info)

if __name__ == '__main__':
    url = 'https://austin.craigslist.org/search/fua?query=bed'
    main(url)