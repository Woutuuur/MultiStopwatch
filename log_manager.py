from datetime import datetime
import util.html2clipboard as h2c
from config import *
from util.time_util import convert_time
from timeframe import Timeframe

ics_base = ''' 
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//woutuuur//MultiStopwatch//EN
BEGIN:VEVENT
UID:MultiStopwatch
TZID:Europe/Amsterdam
DTSTAMP:*DTSTAMP*
DTSTART:*DTSTART*
DTEND:*DTEND*
SUMMARY:*TITLE*
END:VEVENT
END:VCALENDAR
'''


def open_in_outlook(timeframes):
    dtstamp = __to_ics_time_format(datetime.now())
    dtstart = __to_ics_time_format(min(x.start for x in timeframes))
    dtend = __to_ics_time_format(max(x.end for x in timeframes))
    mins = int(round(sum(map(Timeframe.get_time_delta_in_minutes, timeframes))))
    hrs = mins // 60
    time_s = str(mins)
    if hrs > 0:
        mins %= 60
        time_s = f"{hrs}:{mins:02}"
    filename = FULL_PATH + "/_tmp.ics"
    customer = timeframes[0].customer
    title = f"{time_s} - {customer}"
    s = ics_base\
        .replace("*DTSTAMP*", dtstamp)\
        .replace("*DTSTART*", dtstart)\
        .replace("*DTEND*", dtend)\
        .replace("*TITLE*", title)
    with open(filename, "w") as f:
        f.write(s)
    os.startfile(filename)


def __to_ics_time_format(time):
    return str(time.isoformat()).replace('-', '').replace(':', '').split('.')[0]


def copy_logs_to_clipboard(timeframes: list[Timeframe]):
    if len(timeframes) == 0:
        h2c.PutHtml("")
        return
    h2c.PutHtml(timeframes_to_table(timeframes))


def timeframes_to_table(timeframes):
    total = sum(map(Timeframe.get_time_delta_in_seconds, timeframes))

    text = '''<body><table cellspacing="0" border="1">'''
    text += "<tr><th>Datum</th><th>Start</th><th>Einde</th><th>Duratie</th></tr>"
    text += ''.join(map(Timeframe.to_html_row, timeframes))
    text += f'''<tr><td colspan="3"><b>Totaal</b><td>{convert_time(total) }</td></tr>'''
    text += "</table></body>"
    text += "<style>table, th, td{ padding: 10px; border: 1px solid black; border-collapse: collapse; }</style>"
    return text
