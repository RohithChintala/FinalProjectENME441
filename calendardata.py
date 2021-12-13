import requests
from datetime import datetime, timedelta
import urllib.parse
import json
import pytz

#########ONLINE TUTORIAL CODE
GCALENDAR_URL_TEMPLATE = "https://clients6.google.com/calendar/v3/calendars/ii4b21lg3kh8rqbporo8bkb6ms@group.calendar.google.com/events?calendarId=ii4b21lg3kh8rqbporo8bkb6ms%40group.calendar.google.com&singleEvents=true&timeZone=America%2FNew_York&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin=2021-11-28T00%3A00%3A00-05%3A00&timeMax=2022-01-02T00%3A00%3A00-05%3A00&key=AIzaSyBNlYH01_9Hc5S1J9vuFmu2nUqBZJNAXxs"
LOCAL_TIMEZONE = "America/New_York"  # Replace this with your time zone.

def getcalendardata():
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
    #######END OF ONLINE TUTORIAL CODE

    month = [0] * len(parsed_response["items"]) #sets month to be list of empty array with the length of the amount of events
    day = [0] * len(parsed_response["items"])  #sets day to be list of empty array with the length of the amount of events
    hour = [0] * len(parsed_response["items"])  #sets hour to be list of empty array with the length of the amount of events
    minute = [0] * len(parsed_response["items"])  #sets minute to be list of empty array with the length of the amount of events
    i = 0 #sets variable i i to initially be 0
    wakeuptime = 23 #sets wakeuptime to be the highest hour
    wakeminute = 59 #sets wakeminute to be the highest minute
    now = timezone.localize(datetime.now()) #collects the current local time
    currentmonth = now.strftime("%m") #gets the current month
    currentday = now.strftime("%d")#gets the current day
    currenthour = now.strftime("%H") #gets the current hour
    currentminute = now.strftime("%M") #gets the current minute
    wake = [0,0] #initially sets wake to be 0,0
    for event in parsed_response["items"]: ####ONLINE CODE runs through all events in json
        event_start = datetime.fromisoformat(event["start"]["dateTime"])  ####ONLINE CODE collects event start data in event_start
        event_end = datetime.fromisoformat(event["end"]["dateTime"])  ####ONLINE CODE  
        month[i] = event_start.strftime("%m") #fills the month array with months of events
        day[i] = event_start.strftime("%d") #fills day array with days of events
        hour[i] = event_start.strftime("%H") #fills hour array with hours of events
        minute[i] = event_start.strftime("%M") #fils minute array with minutes of events
        if int(day[i]) == 1: #if the day is the first of the month increases that one day by 1 and subtracts that month by 1 to get through the following if statements
          day[i] +=1 #keeps code running on the first of the month
          month[i] -= 1 
        if int(month[i]) == int(currentmonth): #runs if the month of the event is equal to the current month
          if int(day[i]) == int(currentday): #removed + 1 for testing purposes, runs if the day of the event is equal to the current day + 1
            if int(hour[i]) < wakeuptime: #checks if the hour of a given even it less than the current set wakeuptime
              wakeuptime = int(hour[i]) #if hour is less then sets wakeuptime to be equal to that hour
            if int(hour[i]) == wakeuptime: #if the hour is equal to the current wakeuptime 
              if int(minute[i]) <= wakeminute: #checks if the minutes of the event are lower than the current wakeminute or equal
                wakeminute = int(minute[i]) #sets wakeminute to be the events minute
              wakeuptime = int(hour[i]) #sets wakeuptime to be the events hour
            wake = [wakeuptime, wakeminute] #sets wake array to be made of wakeuptime, wakeminute
          i += 1 #increases i by 1 
    return wake #returns wake