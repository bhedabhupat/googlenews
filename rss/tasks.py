from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
import feedparser
from .models import RssData
from googlenews.celery import app
import datetime


@periodic_task(
    run_every=(crontab(hour="*", minute="*/5")),
    name="run_every_5_minutes",
    ignore_result=True
)
def get_rss():
    feed = feedparser.parse("https://news.google.com/rss/search?pz=1&cf=all&q=nse$&hl=en-IN&gl=IN&ceid=IN:en")
    for items in feed['items']:
        pub_date = datetime.datetime.strptime(items['published'], "%a, %d %b %Y %H:%M:%S %Z")
        check_exists = RssData.objects.filter(
            guid=items['guid']
        ).first()
        if not check_exists:
            RssData.objects.create(
                title=items['title'],
                link=items['link'],
                guid=items['guid'],
                pub_date=pub_date,
                description=items['description'],
                source=items['source']['title'],
            )
