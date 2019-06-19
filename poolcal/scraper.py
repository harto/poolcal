from datetime import date, datetime, timedelta
import sys

from bs4 import BeautifulSoup
import requests

DAY_NAMES = 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split()
DAYS = {day: i for i, day in enumerate(DAY_NAMES)}
TIME_FORMAT = '%I:%M %p'

def parse_schedule(url):
    """
    Fetch ``url`` and extract a list of scheduled activities from the HTML.
    """
    resp = requests.get(url, params=None, headers={'User-Agent': 'poolcal'})
    html = BeautifulSoup(resp.content, features='html.parser')
    h3s = [h3 for h3 in html.find_all('h3') if h3.text in DAYS]
    activities = []
    for h3 in h3s:
        table = find_associated_table(h3)
        if not table:
            print('warning: no %s schedule found at %s' % (h3.text, url), file=sys.stderr)
            continue
        for tbody in table.find_all('tbody'):
            activities.append(parse_activity(h3.text, tbody.tr))
    return activities

def find_associated_table(h3):
    # The h3s and tables are all at the same level, so we can't just
    # find_next_sibling('table'), because we might jump over the next heading
    # and get the schedule for the wrong day.
    el = h3.next_sibling
    while el and el.name != 'table' and el.name != 'h3':
        el = el.next_sibling
    return el if el and el.name == 'table' else None

def parse_activity(day_name, tr):
    name, raw_start_time, raw_end_time, _, _, _, raw_start_date, raw_end_date = [
        td.text for td in tr('td')[0:8]
    ]
    period_start = parse_date(raw_start_date)
    period_end = parse_date(raw_end_date)
    start_time = parse_time(raw_start_time)
    end_time = parse_time(raw_end_time)
    return {
        'name': name,
        'start_date': first_occurrence_of_weekday(period_start, day_name),
        'end_date': last_occurrence_of_weekday(period_end, day_name),
        'start_time': start_time,
        'end_time': end_time,
    }

def parse_date(d):
    month, day, year = [int(part) for part in d.split('/')]
    return date(year=year, month=month, day=day)

def parse_time(t):
    return datetime.strptime(t, TIME_FORMAT).time()

def first_occurrence_of_weekday(start_date, day_name):
    d = start_date
    while d.weekday() != DAYS[day_name]:
        d += timedelta(days=1)
    return d

def last_occurrence_of_weekday(end_date, day_name):
    d = end_date
    while d.weekday() != DAYS[day_name]:
        d += timedelta(days=-1)
    return d

if __name__ == '__main__':
    print('\n'.join(sorted(map(repr, parse_schedule(sys.argv[1])))))
