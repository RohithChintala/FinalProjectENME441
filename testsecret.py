import requests
from datetime import datetime, timedelta
import urllib.parse
import json
import pytz

# Replace this with the URL template corresponding to your calendar's events
GCALENDAR_URL_TEMPLATE = "https://clients6.google.com/calendar/v3/calendars/ii4b21lg3kh8rqbporo8bkb6ms@group.calendar.google.com/events?calendarId=ii4b21lg3kh8rqbporo8bkb6ms%40group.calendar.google.com&singleEvents=true&timeZone=America%2FNew_York&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2021-10-31T00%3A00%3A00-05%3A00&timeMax=2021-12-05T00%3A00%3A00-05%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"
LOCAL_TIMEZONE = "America/New_York"  # Replace this with your time zone.

def get_busy_times_from_google_calendar():
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
    busy_times = []
    day = [0] * len(parsed_response["items"])
    hour = [0] * len(parsed_response["items"])
    minute = [0] * len(parsed_response["items"])
    i = 0
    wakeuptime = 23
    wakeminute = 59
    now = timezone.localize(datetime.now()) 
    currentday = now.strftime("%d")
    currenthour = now.strftime("%H")
    currentminute = now.strftime("%M")
    wake = [0,0]
    for event in parsed_response["items"]:
        event_start = datetime.fromisoformat(event["start"]["dateTime"])
        event_end = datetime.fromisoformat(event["end"]["dateTime"])
        
        # Do not include all-day events.
        if event_end - event_start == timedelta(days=1):
            continue
            
        busy_times.append((event_start, event_end))
        print(event_start)
        print(event_start.strftime("%H"),event_start.strftime("%M"))

        day[i] = event_start.strftime("%d")
        hour[i] = event_start.strftime("%H")  
        minute[i] = event_start.strftime("%M")   
        print(day[i],hour[i],minute[i],currentday)
        if int(day[i]) == int(currentday)+1:
          if int(hour[i]) < wakeuptime:
            wakeuptime = int(hour[i])
            print('wake up by',wakeuptime)
          if int(hour[i]) == wakeuptime:
            if int(minute[i]) < wakeminute:
              wakeminute = int(minute[i])
            wakeuptime = int(hour[i])
            print('wake up by',wakeuptime, wakeminute)
            wake = [wakeuptime, wakeminute]
        i += 1
    return busy_times, wake, currentday



def check_if_busy(busy_times, time_to_check):
    """Checks if I am busy at a given time. Returns True if busy, False if free."""
    return any(
        [start_time <= time_to_check <= end_time for start_time, end_time in busy_times]
    )


def main():
  timezone = pytz.timezone(LOCAL_TIMEZONE)
  now = timezone.localize(datetime.now())
  currenthour = now.strftime("%H")
  currentminute = now.strftime("%M")
  if int(currenthour) == 23:
    if int(currentminute) == 0:
      busy_times, wake, currentday = get_busy_times_from_google_calendar()
      busy_right_now = check_if_busy(busy_times, now)
      hour = [wake[0]]
      minute = [wake[1]]
      h = 1
      m = 15
      morningh = int(wake[0])- h
      morningm = int(wake[1])- m
      if morningm < 0:
          morningh -= 1
          morningm = 60 - m
      if morningh < 0:
        morningh = 24 + morningh
      print(morningh, morningm)
      sh = 8
      sm = 30
      nighth = morningh - sh
      nightm = morningm - sm
      if nightm < 0:
          nighth -= 1
          nightm = 60 - sm
      if nighth < 0:
        nighth = 24 + nighth
      print(nighth, nightm)

      if int(currenthour) == int(nighth):
        if int(currentminute) == int(nightm):
          print('nightalarm')
      if int(currenthour) == int(morningh):
        if int(currentminute) == int(morningm):
          print('dayalarm')




if __name__ == "__main__":
    main()
