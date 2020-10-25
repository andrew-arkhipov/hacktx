import scraper
import requests

def get_recommendations(budget=100, furnitures=['bed', 'table', 'desk', 'chair'], num_results=20):
	# url = 'https://austin.craigslist.org/search/apa?query=low income'
	url = 'https://austin.craigslist.org/search/fua?query='
	res = {}
	for item in furnitures:
		html = requests.get(url + item).text
		s = scraper.Scraper(html)
		info = s.find(scraper.CraigslistListing)
		sorted_info = sorted(info)
		relevant_info = list(filter(lambda x: x.price_int > 0, sorted_info))
		res[item] = relevant_info[:num_results]

	''' Budget calculation - Same number of items per category as long as under budget '''
	idx = 0
	budget_res = {}
	while (idx < num_results):
		total = 0
		for item in res:
			total += res[item][idx].price_int
		if total > budget:
			break
		for item in res:
			if item in budget_res:
				budget_res[item].append(res[item][idx])
			else:
				budget_res[item] = [res[item][idx]]
		idx += 1
	return budget_res

if __name__ == '__main__':
	get_recommendations()
