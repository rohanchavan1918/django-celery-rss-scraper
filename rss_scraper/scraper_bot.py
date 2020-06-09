
import feedparser,requests,re
import pandas,csv
from .models import ScrapedData

'''
Benchmark :- Initial RUn :- CSV :- 08.13.83
             After Next 15 mins :- CSV :- 6 sec
Working :-
1. Get all the titles, which are already present ans store in a list.
2. Iterate the URL LIst and get Feed.
3. Iterate through the entries of all the Feed.
4. If the entry['title'] is not present in the "already present" list then add
'''

# The XML of INdiatoday links doesnot return proper output in the description,
# Get the proper title by sending a get req at the endpoint and then filter the description using regex.
def GetDesc(link):
    # print("Domain is of NDTV ",FindDomain(link))
    resp_text = requests.get(link).text #store response in resp_text
    pattern = re.compile('<div class="story-kicker"><h2>(.*?)</h2></div>')
    desc = pattern.findall(str(resp_text))
    if desc == []:
        # handle WORST CASE SCENARIO if no desc is found
        return "NOT-FOUND"
    return desc[0] #Proper SUmmary

def GetCurrentList():
    titles = ScrapedData.object.all().values('Title')
    # print(names)
    return titles


# Find Domain from the URL
def FindDomain(url):
    domain = url.split("://")[1].split("/")[0] 
    return domain

def MasterScraper():
    # List of URLs to Scrape
    url_list = [
        "https://www.indiatoday.in/rss/1206514",
        "https://www.indiatoday.in/rss/1206614",
        "https://www.indiatoday.in/rss/1206584",
        "https://www.indiatoday.in/rss/1206513",
        "https://www.indiatoday.in/rss/1206577",
        "https://feeds.feedburner.com/ndtvnews-top-stories",
        "https://feeds.feedburner.com/ndtvnews-latest",
        "https://feeds.feedburner.com/ndtvnews-india-news", 
        "https://feeds.feedburner.com/ndtvnews-world-news",
        "https://feeds.feedburner.com/ndtvprofit-latest",
    ]

    # Main
    AlreadyPresentTitles = GetCurrentList()
    print(AlreadyPresentTitles)
    # First get all the titles in DB , Objects.all().values('title), if new title is not present then add it to the db

    # with open('database.csv',mode='a+',newline='',encoding="utf-8",errors='replace') as database:
    #     # database_writer = csv.writer(database,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     database_writer = csv.writer(database,delimiter=',')
    #     # Iterate the URL POOL
    #     for url in url_list:
    #         feeds = feedparser.parse(url)
    #         DomainCheck = FindDomain(url)
    #         if DomainCheck == "www.indiatoday.in":
    #             # IndiaTOday WEbsite, Scrap the desc from site.
    #             for feed in feeds.entries:
    #                 # Check if it is already present, pass if it is present,else write it
    #                 if feed['title'] not in AlreadyPresentTitles:
    #                     # print("Title :- ",feed['title'],"\n Summary :-",GetDesc(feed['link']),"\n Date",feed['published'],"\n Link :-",feed['link'])
    #                     list_to_append = [feed['title'],GetDesc(feed['link']),feed['published'],feed['link']]
    #                     database_writer.writerow(list_to_append)
    #         elif DomainCheck == "feeds.feedburner.com":
    #             # feedBUrner , no need to scrap desc from website
    #             for feed in feeds.entries: # For Feed BUrner
    #                 if feed['title'] not in AlreadyPresentTitles:
    #                     # print("Title :- ",feed['title'],"\n Summary :-",feed['summary'],"\n Date",feed['published'],"\n Link :-",feed['link'])
    #                     list_to_append = [feed['title'],feed['summary'],feed['published'],feed['link']]
    #                     database_writer.writerow(list_to_append)
        # print("---------------------")

if __name__ == '__main__':
    MasterScraper()
# MasterScraper()



'''
Convert date into date time object
____________________________________-
from dateutil import parser as date_parser
import datetime
date_str = "Wed, 03 Jun 2020 02:19:30 GMT"
newDate = date_parser.parse(date_str).date()
'''