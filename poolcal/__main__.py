import os.path
from sys import argv, stdout

from poolcal.calendar import generate_calendar
from poolcal.scraper import parse_schedule

ROOT = os.path.join(os.path.dirname(__file__), '..')
SOURCES = os.path.join(ROOT, 'sources.txt')

def main():
    feeds = []
    with open(SOURCES) as sources:
        for line in sources:
            line = line.rstrip('\n')
            if not line: continue
            url, name = line.split('\t', 2)
            try:
                schedule = parse_schedule(url)
            except Exception as e:
                raise Exception(f'error parsing {url}', e)
            calendar = generate_calendar(name, schedule)
            filename = name.lower().replace(' ', '-') + '.ical'
            relpath = os.path.join('feeds', filename)
            path = os.path.join(ROOT, relpath)
            with open(path, 'w') as calfile:
                calfile.buffer.write(calendar.to_ical())
            feeds.append((name, relpath))

    with open(os.path.join(ROOT, 'index.html'), 'w') as index:
        index.write(HTML_TEMPLATE % {
            'feeds': '\n      '.join(
                f'<li><a href="{path}">{name}</a></li>'
                for name, path in feeds
            )
        })

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
  <body>
    <ul>
      %(feeds)s
    </ul>
  </body>
</html>
"""

if __name__ == '__main__':
    main()
