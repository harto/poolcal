from icalendar import Calendar, Event, vDatetime
from poolcal.scraper import scrape
from sys import argv, stdout
import tempfile

def main():
    url = argv[1]
    result = scrape(url)
    pool_name = result['name']
    schedule = result['schedule']
    cal = Calendar()
    cal['name'] = pool_name
    cal['x-wr-calname'] = pool_name
    uid = 0
    for weekday in schedule:
        for activity in weekday:
            event = Event()
            event['summary'] = f'{pool_name} - {activity["name"]}'
            event['dtstart'] = vDatetime(activity['start_time'])
            event['dtend'] = vDatetime(activity['end_time'])
            event['rrule'] = 'FREQ=WEEKLY'
            cal.add_component(event)
    stdout.buffer.write(cal.to_ical())

if __name__ == '__main__':
    main()
