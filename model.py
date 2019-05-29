# Importing Modules
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from datetime import datetime as dt
from collections import defaultdict
import pandas as pd
from pandas import DataFrame
from time import strftime, gmtime
import redis
import os

r = redis.from_url("redis://localhost:6379")
# os.environ.get("REDIS_URL")
# Generate a URL with a specified page number and city
def generate_url(page_number = 1):
    if page_number == 1:
        return f"https://www.naukri.com/jobs-in-bangalore"
    return f"https://www.naukri.com/jobs-in-bangalore-{page_number}"    

# Generate a query string with inputs of freshness and city name
def generate_query(**kwargs):
    freshness = kwargs.get("freshness","")
    if freshness in [1,7]:
        qo = freshness
        qco = freshness
    elif freshness == 3:
        qo = 2
        qco = 2    
    elif freshness == 15:
        qo = 1
        qco = 15
    elif freshness == 30:
        qo = 6
        qco = 66
    else:
        qo = ""
        qco = ""            
    dictionary = {
        'ql': kwargs.get("cities",""),
        'qo': qo,
        'qco[]': qco
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

# Checks if there's a next page
def next_page(soup):
    gray_btn = soup.findAll('button',{'class':'grayBtn'})
    try:
        if len(gray_btn) == 1 and gray_btn[0].text == "Previous":
            return False
        else:
            return True
    except:
        return False


# This function takes a Naukri page and scrapes certain information
def scrape_page(soup, page):
    data_divs=soup.find_all("div", {"type" : "tuple" })
    data_dict = defaultdict(list)
    for data_div in data_divs:
        data_dict['Page No.'].append(page)
        try : 
            data_dict['url'].append(data_div['data-url'])
            data_dict['organization'].append(data_div.find(attrs={"class": "org"}).text)
            data_dict['title'].append(data_div.find(attrs={"class": "desig"}).text)
            try:
                data_dict['experience'].append(data_div.find(attrs={"class": "exp"}).text)
            except:
                data_dict['experience'].append(None)
            try:          
                data_dict['skill'].append(data_div.find(attrs={"class": "skill"}).text)
            except:
                data_dict['skill'].append(None)
            try:
                data_dict['description'].append(data_div.find_all(attrs={"class": "more desc"})[1].text)
            except:
                data_dict['description'].append(None)            
            data_dict['salary'].append(data_div.find(attrs={"class": "salary"}).text)
            data_dict['postedby'].append(data_div.find(attrs={"class": "rec_name"}).text)
            data_dict['time'].append(data_div.find(attrs={"class": "date"}).text)
            data_dict['runtime']=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        except:
            data_dict['url'].append(None)
            data_dict['organization'].append(None)
            data_dict['title'].append(None)
            data_dict['experience'].append(None)
            data_dict['skill'].append(None)
            data_dict['description'].append(None)
            data_dict['salary'].append(None)
            data_dict['postedby'].append(None)
            data_dict['time'].append(None) 
            data_dict['runtime']=strftime("%Y-%m-%d %H:%M:%S", gmtime())          
    return DataFrame(data_dict)


# This is the main function that links everything
def scraper(**kwargs):
    page_limit = kwargs.pop("page_limit",1000000000000000000)
    query = generate_query(**kwargs)
    next_check = True
    page = 1
    final = DataFrame()
    start = dt.now()
    r.set("page",0)
    while next_check and page <= page_limit:
        url = generate_url(page)
        request = requester(url, query)
        if request.status_code != 200:
            total_time = dt.now() - start
            print("We got a faulty status code.")
            r.set("page","Faulty Status Code")
            return final, total_time
        soup = BeautifulSoup(request.content, "lxml")
        data = scrape_page(soup,page)
        final = pd.concat([final,data])
        next_check = next_page(soup)
        print(f"Finished scraping page {page}...")
        r.incr("page")
        page += 1
    total_time = dt.now() - start
    r.set("page","Done!")    
    return final, total_time