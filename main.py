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
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://www.naukri.com/jobs-in-bangalore",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "414",
    "DNT": "1",
    "Connection": "close",
    "Cookie": "test=naukri.com; _t_ds=0951766001558009576-B080434FB822-5AC165574317; _t_us=5CDD56E8; _t_s=direct; _t_r=1091%2F%2F; PHPSESSID=26e07d8d3b0ad325e5896ca05b3b8f95; ak_bmsc=351DEFEA5707E39A41341432CDE272C217201D744F5A0000E956DD5C94D5046B~plMc3hmd++vWNIinGdP4TP9aqXKNEHNTHTIELxXF7AaT+ndn0ze3Ve7kAGOcOof+TXBkcQgvqnvVxtvHakdfbsOI7s9mzge+GPuFmIDLA31Y5tTimA48VJRabDcUH/qrb5CBc1I5fIByZtLsZCYh9eu1A0yvyXvWe4RdBTtISOg5eFW9iEHWcRvGOZUh6dfyytEwH6et7g8qF3z51gz5HUxGFDi17Yyh0mcAqrBlFBGT5d37MMzPZ75M7tC/+qW+jx; MYNAUKBMS[resolution]=640; bm_sv=8F87AD4618CEC572F4E3C1E59A2BAE0C~NVf9rkUwwqYE2kJP6+jNq0NZ7RSqoiim/SPoLA1b+Jt7CAdKnubpeD0Kmg9wz3V30/fJ/rwyytxXEyMMKLJak80cJ6HBIqC6JXGsziB0DxNSpn8wccNMPssWWtmDQFjehafE6arCtFEJWX3dvacNHA==; HOWTORT=cl=1558009585346&r=https%3A%2F%2Fwww.naukri.com%2Fjobs-in-bangalore&nu=https%3A%2F%2Fwww.naukri.com%2Fjobs-by-location&ul=1558009617443&hd=1558009601063",
    "Upgrade-Insecure-Requests": "1"}

    request = requests.post(url,data = query, headers = headers)

    return request



    



