from __future__ import absolute_import, unicode_literals
from celery import task
from .models import ScrapedData
# Requirements for Bot
import feedparser,requests,re
from dateutil import parser as date_parser
import datetime
import logging

logger = logging.getLogger(__name__)


'''
Working of the Bot :-
1) In the Initial Scrap all the data and add it to DB
2) From Second Iteration onwards --
    - First get all titles saved in DB and save it in list
    - Scrap all the URLS, if the title is already in list, means it is in DB,
      No Need to Hit the DB.
    - If Data is Not in list,add it to DB
    (This will reduce the DB hits in every iteration)
    Redis could also be used,Instead of Checking from a local list, which would make it even more faster.
'''

# GetDesc returns Description of indiatoday
def GetDesc(link):
    try:
        resp_text = requests.get(link).text #store response in resp_text
        pattern = re.compile('<div class="story-kicker"><h2>(.*?)</h2></div>')
        desc = pattern.findall(str(resp_text))
        if desc == []:
            # handle WORST CASE SCENARIO if no desc is found
            logger.error('Something went wrong!')
            return "NOT-FOUND"
        return desc[0]
    except Exception as ReqErr:
        logger.error('Error in GetDesc - Request ERROR.',ReqErr)
        return "NOT-FOUND"

# GetCurrentList returns a list of all the titles present in the database.
def GetCurrentList():
    titles = list(ScrapedData.objects.values_list('Title',flat=True))
    return titles

# ConvertDate takes input in format "Wed, 03 Jun 2020 02:19:30 GMT" and returns datetime object
def ConvertDate(date_str):
    FormatedDate = date_parser.parse(date_str).date()
    return FormatedDate

# FindDomain is a helper function to get the domain to distinguish domains (NDTV Domains need to run GetDesc())
def FindDomain(url):
    domain = url.split("://")[1].split("/")[0] 
    return domain

# AddToDatabase Adds a row to DB.# Input :- Title,Description,Date,url
def AddToDatabase(title,description,date,url):
    try:
        ScrapedData.objects.create(Title=title,Description=description,Date=date,url=url)
        print("[+] Added ",title) #DEBUG
    except Exception as DataCreateError:
        logger.error('[!] ERROR WHILE ADDING TO DB :- ',title,description,date,url)
        pass

# Checks if a value is already present in a db
def AlreadyPresentDatabase(title):
    try:
        if ScrapedData.objects.filter(Title=title).count() >= 1:
            # Already Preset
            return True
        else:
                # Not present.
            return False
    except Exception as exc:
        logger.error('[!] ERROR WHILE Getting Count :- ',title)
        pass

# CheckIf Value is Present in Table
def AlreadyPresentTitleList(title,TitlesInList):
    if title in TitlesInList:
        return True
    else:
        return False

# MasterScraper -> Main FUnction.
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

    # AlreadyPresentDatabase return True if data is already presnt and false if not. 
    TitlesInList = GetCurrentList()
    
    # Iterate the URL POOL
    for url in url_list:
        feeds = feedparser.parse(url)
        domain = FindDomain(url)
        if domain == "www.indiatoday.in":
            # IndiaTOday WEbsite,Scrap the desc from site.
            for feed in feeds.entries:
                # First Check if value is in table,
                if AlreadyPresentTitleList(feed['title'],TitlesInList) == False:
                    # Value is not in table, Again confirm it is not.
                    if AlreadyPresentDatabase(feed['title']) == False :
                        # print("Title :- ",feed['title'],"\n Summary :-",GetDesc(feed['link']),"\n Date",feed['published'],"\n Link :-",feed['link'])
                        title,description,date,url = feed['title'],GetDesc(feed['link']),ConvertDate(feed['published']),feed['link']
                        # Add To DB
                        AddToDatabase(title,description,date,url)
                    else:
                        pass
                else:
                    pass
        elif domain == "feeds.feedburner.com":
                # feedBUrner , no need to scrap desc from website
            for feed in feeds.entries: # For Feed BUrner
                 # First Check if value is in table,
                if AlreadyPresentTitleList(feed['title'],TitlesInList) == False:
                    if AlreadyPresentDatabase(feed['title']) == False:
                            # print("Title :- ",feed['title'],"\n Summary :-",feed['summary'],"\n Date",feed['published'],"\n Link :-",feed['link'])
                        title,description,date,url = feed['title'],feed['summary'],ConvertDate(feed['published']),feed['link']
                        # Add To DB
                        AddToDatabase(title,description,date,url)
                    else:
                        pass
                else:
                    pass
    print("[+] Iteration Completed.")


@task
def start_scraper():
    print("[+] Starting Scrapper !")
    MasterScraper()
