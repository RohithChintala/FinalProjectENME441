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
    for event in parsed_response["items"]:
        event_start = datetime.fromisoformat(event["start"]["dateTime"])
        event_end = datetime.fromisoformat(event["end"]["dateTime"])
        
        # Do not include all-day events.
        if event_end - event_start == timedelta(days=1):
            continue
            
        busy_times.append((event_start, event_end))

    return busy_times


def check_if_busy(busy_times, time_to_check):
    """Checks if I am busy at a given time. Returns True if busy, False if free."""
    return any(
        [start_time <= time_to_check <= end_time for start_time, end_time in busy_times]
    )


def main():
    # Get the current time.
    timezone = pytz.timezone(LOCAL_TIMEZONE)
    now = timezone.localize(datetime.now())

    # Don't read from cache if the minute is divisible by 5 (e.g. 6:00, 6:05)
    # or if the local cache does not exist
    # or if the local cache has not yet been modified today
    do_not_read_cache = (
        now.minute % 5 == 0
        or not os.path.exists(LOCAL_CACHE_FILEPATH)
        or timezone.localize(
            datetime.fromtimestamp(os.path.getmtime(LOCAL_CACHE_FILEPATH))
        ).date()
        != now.date()
    )

    if do_not_read_cache:
        # Get the busy times from Google Calendar.
        busy_times = get_busy_times_from_google_calendar()

    
    else:
        # Read the busy times and smart plug IP from cache.
        cache = open(LOCAL_CACHE_FILEPATH, "rb")
        cached_data = pickle.load(cache)
        cache.close()
        busy_times = cached_data["busy_times"]

    # If we're outside of workday hours, do nothing except turn the plug off.
    workday_start_time = datetime.strptime(WORKDAY_START, "%I:%M%p").time()
    workday_end_time = datetime.strptime(WORKDAY_END, "%I:%M%p").time()

    # If you can't find the smart plug on the local network, error and exit.

    # Check if I'm busy right now and if so, turn the light on. Otherwise, turn it off


    # Create the cache if it does not exist.
    if not os.path.exists(LOCAL_CACHE_FILEPATH):
        open(LOCAL_CACHE_FILEPATH, "w+").close()

    # Write to the cache
    cache = open(LOCAL_CACHE_FILEPATH, "wb")
    pickle.dump(data_to_write, cache)
    cache.close()

if __name__ == "__main__":
    main()
