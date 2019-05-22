# Importing Modules
import requests
from urllib.parse import urlencode

# Generate a URL with a specified page number
def generate_url(page_number):
    if page_number == 1:
        return f"https://www.naukri.com/jobs-in-bangalore"
    return f"https://www.naukri.com/jobs-in-bangalore-{page_number}"    

# Generate a query string with inputs of freshness and city name
def generate_query(**kwargs):
    dictionary = {
        'ql': kwargs.get("cities",""),
        'qo': kwargs.get("freshness",""),
        'qco[]': kwargs.get("freshness","")
    }
    encoded = urlencode(dictionary)
    return encoded

# Produce and returns the result of the post request
def requester(url,query):
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})

    request = requests.post(url,data = query, headers = headers)

    return request



    



