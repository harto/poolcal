from datetime import datetime

from icalendar import Calendar, Event, vDatetime
from pytz import timezone

TIMEZONE = timezone('US/Pacific')

def make_datetime(date, time):
    dt = datetime.combine(date=date, time=time)
    return TIMEZONE.localize(dt)

def generate_calendar(name, schedule):
    cal = Calendar()
    # TODO: are both needed?
    cal['name'] = name
    cal['x-wr-calname'] = name
    for activity in schedule:
        first_occurrence_start = make_datetime(activity['start_date'], activity['start_time'])
        first_occurrence_end = make_datetime(activity['start_date'], activity['end_time'])
        last_occurrence_end = make_datetime(activity['end_date'], activity['end_time'])
        event = Event()
        event['summary'] = f'{name} - {activity["name"]}'
        event['dtstart'] = vDatetime(first_occurrence_start)
        event['dtend'] = vDatetime(first_occurrence_end)
        event.add('rrule', {
            'freq': 'weekly',
            'until': last_occurrence_end,
        })
        cal.add_component(event)
    return cal
