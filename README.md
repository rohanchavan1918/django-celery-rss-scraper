# Catalyst-Rss-Worker

Catalyst Rss Worker is an automated scraper that asynchronously scrapes a given set of RSS Feeds and saves the title, description, date, and URL to the Postgres database. This tool efficiently handles duplicate data and reduces redundancy, and is optimized to reduce the hits on the database. It uses celery to scrape the feeds every 15 minutes and the Flower dashboard could be used to monitor the tasks performed.

Live:- http://128.199.78.218/ 

## How it works?
1. In the initial dump, the bot scrapes all the title, description, date,URL. it uses [feedparser](https://pypi.org/project/feedparser/) which is a Universal feed parser, handles RSS 0.9x, RSS 1.0, RSS 2.0, CDF, Atom 0.3, and Atom 1.0 feeds.
2. Every next iteration, a list of titles that are already present in the database is stored locally. When the worker runs (every 15 minutes) it first checks whether the title is present in the list or not. If it gets the exact title stored in the list, it will not save it again. This approach makes it fast and also reduce the hits to the database while ensuring that the same data is not stored in the database again. (A faster solution would be to use to redis instead of a list)

# Images
## SignIn
Goto [Login Page](http://128.199.78.218/) and use the credentials to login

![Image](https://drive.google.com/uc?export=view&id=1fybxtfJTGkhD7vEA6LVec28Mc8gIfDb3)

## Scraped Data
After Logging in to the web app, you can now observe all the details of the scraped data.

![Image](https://drive.google.com/uc?export=view&id=1ecIU82FcEjkvQdO0SyIu-oknlkzV6eat)

## Perform Queries
User can perform queries based on the title, description, Url, Data.

### Search by date
![Image](https://drive.google.com/uc?export=view&id=1wLwxfRTWKZgImZC3RPYFIZ7OoDWHlrUq)

### Search by title
![Image](https://drive.google.com/uc?export=view&id=1AWu6St-YsDF6vbbZdHB87M3WoZVWkhuN)

### Search by key words
![Image](https://drive.google.com/uc?export=view&id=1VhUolc6xx39glDL5I8gtN6rlfwEBk-Fj)

### Flower Dashboard
![Image](https://drive.google.com/uc?export=view&id=1r0mCWN74w-UhMo4GygUcLqJNcL_gIIGD)

## Adding/Removing Urls

The Urls of RSS Feeds to scan or delete can be configured easily, by editing the 
`url_list` in `/rss_worker/tasks.py` 

```python
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

```
asd
## Changing the Time of repetition
You can change the time interval in which the worker should run by changing the `CELERY_BEAT_SCHEDULE` in `settings.py`
```python
CELERY_BEAT_SCHEDULE = {
    'start-scraper': {
       'task': 'rss_scraper.tasks.start_scraper',
        # Time Interval of worker (In Seconds)
       'schedule': 900.0,
    },
    }

```


