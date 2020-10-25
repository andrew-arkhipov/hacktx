from . import scraper
import requests
import collections
import json

def get_recommendations(dic, num_results=5):
    city = dic['city'].replace(" ", "")
    budget = int(dic['budget'])
    furnitures = dic['elements']

    url = f'https://{city.lower()}.craigslist.org/search/fua?query='
    res = collections.defaultdict(dict)
    for item in furnitures:
        html = requests.get(url + str(item)).text
        s = scraper.Scraper(html)
        info = s.find(scraper.CraigslistListing)
        sorted_info = sorted(info)
        relevant_info = list(filter(lambda x: x._price_int > 5, sorted_info))[:num_results]
        for tag in relevant_info:
            info = tag.info
            for k, v in info.items():
                res[item][k] = v

    ''' Budget calculation - Same number of items per category as long as under budget '''
    idx = 0
    budget_res = collections.defaultdict()
    while (idx < num_results):
        total = 0
        for item in res.keys():
            total += int(res[item]['price'].lstrip('$'))
        if total > budget:
            break
        for item in res:
            for k, v in res[item].items():
                budget_res[item][k] = str(v)
        idx += 1

    return json.dumps(budget_res)

def get_job_recommendations(dic, num_results=10):
    job_type = dic['role']
    zipcode = dic['zip_code']
    url = 'https://www.indeed.com/jobs?q='+job_type+'&l='+zipcode
    html = requests.get(url).text
    s = scraper.Scraper(html)
    listing_array = sorted(s.find(scraper.JobPosting))
    num_results = len(listing_array) if num_results > len(listing_array) else num_results
    res = list(map(lambda x : x.info, listing_array[:num_results]))
    return res

if __name__ == '__main__':
    dic = {
        'city': 'Austin',
        'budget': '600',
        'elements': ['table', 'chair', 'bed']
    }
    res = get_recommendations(dic)  
    print(res)
