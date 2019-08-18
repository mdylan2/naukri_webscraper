# A Tool to Scrape Job Data from Naukri
## Description
This repository contains files to scrape all the jobs released in specific cities in India on Naukri within a specific time frame.

## List of Files
The repository contains the following files:
- `model.py`: Contains all the functions needed to get all job data
- `complete_city_list.csv`: Contains all cities that can be used as inputs for the `scraper` function in `model.py`

## Installation/Usage
1. Clone the repo onto your computer. 
```
git clone https://github.com/mdylan2/employment_app.git
```
2. Navigate to the folder and open up a Python shell. Import all the functions from `model.py`.
```
Python 3.7.3 (default, Apr 24 2019, 15:29:51) [MSC v.1915 64 bit (AMD64)] :: Anaconda, Inc. on win32

Warning:
This Python interpreter is in a conda environment, but the environment has
not been activated.  Libraries may fail to load.  To activate this environment
please see https://conda.io/activation

Type "help", "copyright", "credits" or "license" for more information.
>>> from model import *
```
3. Run the `scraper` function to scrape data. Currently, the scraper function only accepts the following keyword arguments: cities, freshness, page_limit. Cities can be an item like "bangalore" or a list like ["mumbai", "bangalore"]. Freshness has to be a number of days within which a job was released (at the time of writing, Naukri only accepts 1, 3, 7, 15 or 30 days). Page Limit is where you can set the number of pages you'd like to scrape. Here's an example to scrape all the jobs in Bangalore released over the last 7 days.
```
scraped_naukri_data, time_taken_to_scrape = scraper("bangalore", 7) 
```

## Questions
If you have any questions/issues relating to the scraper, please do not hesitate to contact me on GitHub. 
