import requests
from datetime import datetime, timedelta
import urllib.parse
import json
import pytz

# Replace this with the URL template corresponding to your calendar's events
###GCALENDAR_URL_TEMPLATE = "https://clients6.google.com/calendar/v3/calendars/ii4b21lg3kh8rqbporo8bkb6ms@group.calendar.google.com/events?calendarId=ii4b21lg3kh8rqbporo8bkb6ms%40group.calendar.google.com&singleEvents=true&timeZone=America%2FNew_York&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2021-10-31T00%3A00%3A00-05%3A00&timeMax=2021-12-05T00%3A00%3A00-05%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"

GCALENDAR_URL_TEMPLATE = "https://clients6.google.com/calendar/v3/calendars/ii4b21lg3kh8rqbporo8bkb6ms@group.calendar.google.com/events?calendarId=ii4b21lg3kh8rqbporo8bkb6ms%40group.calendar.google.com&singleEvents=true&timeZone=America%2FNew_York&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2021-11-28T00%3A00%3A00-05%3A00&timeMax=2022-01-02T00%3A00%3A00-05%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"
LOCAL_TIMEZONE = "America/New_York"  # Replace this with your time zone.

def getcalendardata():
    """Returns a list of tuples (start time, end time) that represent busy times."""

    # Headers for the HTTP GET request.
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    # Define a function encode which will take a string as input and return a
    # URL-safe version. For example: "America/New_York" is converted to
    # "America%2FNew_York".
    encode = lambda string: urllib.parse.quote(string, safe="")

    # Get the time at the start of the current day (midnight) in this timezone.
    timezone = pytz.timezone(LOCAL_TIMEZONE)
    start_of_today = timezone.localize(datetime.now()).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_of_tomorrow = start_of_today + timedelta(days=1)

    # Generate the URL with the timezone, start date, and end date parameters.
    url = GCALENDAR_URL_TEMPLATE.format(
        timezone=encode(LOCAL_TIMEZONE),
        start_datetime=encode(start_of_today.isoformat()),
        end_datetime=encode(start_of_tomorrow.isoformat()),
    )

    # Send the request, get the response, parse it.
    response = requests.get(url, headers=headers)
    parsed_response = json.loads(response.text)

    # Get the start and end times from all of the events.
    month = [0] * len(parsed_response["items"])
    day = [0] * len(parsed_response["items"])
    hour = [0] * len(parsed_response["items"])
    minute = [0] * len(parsed_response["items"])
    i = 0
    wakeuptime = 23 
    wakeminute = 59
    now = timezone.localize(datetime.now()) 
    currentmonth = now.strftime("%m")
    currentday = now.strftime("%d")
    currenthour = now.strftime("%H")
    currentminute = now.strftime("%M")
    wake = [0,0]
    for event in parsed_response["items"]:
        event_start = datetime.fromisoformat(event["start"]["dateTime"])
        event_end = datetime.fromisoformat(event["end"]["dateTime"])  
        month[i] = event_start.strftime("%m")
        day[i] = event_start.strftime("%d")
        hour[i] = event_start.strftime("%H")  
        minute[i] = event_start.strftime("%M")   
        if int(day[i]) == 1:
          day[i] +=1 #keeps code running on the first of the month
        if int(month[i]) == int(currentmonth):
          if int(day[i]) == int(currentday)+1:
            if int(hour[i]) < wakeuptime:
              wakeuptime = int(hour[i])
            if int(hour[i]) == wakeuptime:
              if int(minute[i]) < wakeminute:
                wakeminute = int(minute[i])
              wakeuptime = int(hour[i])
              wake = [wakeuptime, wakeminute]
          i += 1
    return wake, currentday