import scraper
import requests

def get_recommendations(budget=500, furnitures=['bed', 'table', 'desk', 'chair'], num_results=3):
	# url = 'https://austin.craigslist.org/search/apa?query=low income'
	url = 'https://austin.craigslist.org/search/fua?query='
	res = {}
	for item in furnitures:
		html = requests.get(url + item).text
		s = scraper.CraigslistScraper(html)
		info = s.find(scraper.CraigslistListing)
		relevant_info = list(filter(lambda x: x.price_int > 10, info))
		res[item] = relevant_info[:num_results]
	return res

if __name__ == '__main__':
	get_recommendations()
