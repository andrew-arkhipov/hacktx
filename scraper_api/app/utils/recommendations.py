from . import scraper
import requests
import collections

def get_recommendations(num_results=20, **kwargs):
    city = kwargs['city'].replace(" ", "")
    budget = int(kwargs['budget'])
    furnitures = kwargs['elements']

    url = f'https://{city.lower()}.craigslist.org/search/fua?query='
    res = {}
    for item in furnitures:
        html = requests.get(url + item).text
        s = scraper.Scraper(html)
        info = s.find(scraper.CraigslistListing)
        sorted_info = sorted(info)
        relevant_info = list(filter(lambda x: x._price_int > 5, sorted_info))
        descriptions = [tag.info for tag in relevant_info]
        res[item] = descriptions[:num_results]

    ''' Budget calculation - Same number of items per category as long as under budget '''
    idx = 0
    budget_res = collections.defaultdict(dict)
    while (idx < num_results):
        total = 0
        for item in res:
            total += res[item][idx]._price_int
        if total > budget:
            break
        for item in res:
            for desc in item:
                budget_res[item][desc] = res[item][desc]
        idx += 1

    return budget_res

def get_job_recommendations(zipcode='78705', job_type='No+Experience', num_results=10):
    url = 'https://www.indeed.com/jobs?q='+job_type+'&l='+zipcode
    html = requests.get(url).text
    s = scraper.Scraper(html)
    listing_array = sorted(s.find(scraper.JobPosting))
    num_results = len(listing_array) if num_results > len(listing_array) else num_results
    res = list(map(lambda x : x.info, listing_array[:num_results]))
    return res

if __name__ == '__main__':
    res = get_recommendations()
    print(res)
