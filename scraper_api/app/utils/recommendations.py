from . import scraper
import requests
import collections
import json

def get_recommendations(dic, num_results=10):
    city = dic['city'].replace(" ", "")
    budget = int(dic['budget'])
    furnitures = dic['elements']

    url = f'https://{city.lower()}.craigslist.org/search/fua?query='
    res = collections.defaultdict(list)
    for item in furnitures:
        html = requests.get(url + str(item)).text
        s = scraper.Scraper(html)
        info = s.find(scraper.CraigslistListing)
        sorted_info = sorted(info)
        relevant_info = list(filter(lambda x: x._price_int > 5, sorted_info))[:num_results]
        for tag in sorted_info[:num_results]:
            info = tag.info
            res[item].append(info)

    ''' Budget calculation - Same number of items per category as long as under budget '''
    idx = 0
    budget_res = {}
    while (idx < num_results):
        total = 0
        for item in res.keys():
            total += float(res[item][idx]['price'].lstrip('$'))
        if total > budget:
            break
        for item in res:
            record = {}
            for k, v in res[item][idx].items():
                record[k] = str(v)
            if item in budget_res:
                budget_res[item].append(record)
            else:
                budget_res[item] = [record]
        idx += 1

    return budget_res


def get_housing_recommendations(dic, num_results=5):
    city = dic['city'].replace(" ", "")
    zipcode = dic['zip_code'].replace(" ", "")
    budget = dic['budget']

    url = f'https://{city.lower()}.craigslist.org/search/apa?postal={zipcode}&maxprice={budget}'
    html = requests.get(url).text
    s = scraper.Scraper(html)
    tags = s.find(scraper.Housing)

    res = {'apartments': []}
    i = 0
    while i < num_results:
        info = tags[i].info
        res['apartments'].append({k: str(v) for k, v in info.items()})
        i += 1
    return res

def get_job_recommendations(dic, num_results=15):
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
        'zipcode': '78705',
        'budget': '600',
        'elements': ['table', 'chair']
    }
    #res = get_housing_recommendations(dic)  
    res = get_recommendations(dic)
    print(res)
