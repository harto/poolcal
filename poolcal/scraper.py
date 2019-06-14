from bs4 import BeautifulSoup
from pytz import timezone
import requests
from datetime import date, datetime, timedelta

DAY_NAMES = 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split()
DAYS = {day: i for i, day in enumerate(DAY_NAMES)}
TIME_FORMAT = '%I:%M %p'
TIMEZONE = timezone('US/Pacific')

def scrape(url):
    resp = requests.get(url, params=None, headers={'User-Agent': 'poolcal'})
    html = BeautifulSoup(resp.content, features='html.parser')
    return {
        'name': html.find('h1', {'class': 'page-title'}).text,
        'schedule': parse_schedule(html),
    }

def parse_schedule(html):
    h3s = [h3 for h3 in html.find_all('h3') if h3.text in DAYS]
    return [parse_day(h3.text, h3.find_next_sibling('table')) for h3 in h3s]

def parse_day(day_name, table):
    return [parse_event(day_name, tbody.tr) for tbody in table('tbody')]

def parse_event(day_name, tr):
    name, start_time, end_time = [td.text for td in tr('td')[0:3]]
    return {
        'name': name,
        'start_time': parse_datetime(day_name, start_time),
        'end_time': parse_datetime(day_name, end_time),
    }

# TODO: this will all need to take into account the date ranges to which these
# times apply

def parse_datetime(day_name, t):
    dt = datetime.combine(date=next_weekday_occurrence(day_name),
                          time=datetime.strptime(t, TIME_FORMAT).time())
    return TIMEZONE.localize(dt)

def next_weekday_occurrence(day_name):
    if day_name not in DAYS:
        raise ValueError(day_name)
    start = date.today()
    while start.weekday() != DAYS['Monday']:
        start = start + timedelta(days=1)
    return start + timedelta(days=DAYS[day_name])
