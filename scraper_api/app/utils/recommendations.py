import scraper
import requests

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
        res[item] = relevant_info[:num_results]

    ''' Budget calculation - Same number of items per category as long as under budget '''
    idx = 0
    budget_res = {}
    while (idx < num_results):
        total = 0
        for item in res:
            total += res[item][idx]._price_int
        if total > budget:
            break
        for item in res:
            if item in budget_res:
                budget_res[item].append(res[item][idx])
            else:
                budget_res[item] = [res[item][idx]]
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
