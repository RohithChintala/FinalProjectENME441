import requests
from datetime import datetime, timedelta
import urllib.parse
import json
import pytz
import RPi.GPIO as GPIO
import time
import json
from calendardata import get_busy_times_from_google_calendar
import LCD1602
from passiveBuzzer import buzzsetup, buzzloop, buzzdestroy
GPIO.setmode(GPIO.BCM)

buttonPin = 5
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
currenthour = 1
nighth = 1
currentminute = 1
nightm = 1

morningh = 2
morningm = 2

LCD1602.init(0x27, 1)

if int(currenthour) == int(nighth):
  if int(currentminute) == int(nightm):
    print('nightalarm') ###where alarm goes
    LCD1602.write(5, 0, '%s:%s' % (currenthour,currentminute))
    LCD1602.write(2, 1, 'Time To Sleep')
    buzzsetup()
    buzzloop()
    if GPIO.input(buttonPin) == 1:
      buzzdestroy()
      LCD1602.write(0, 1, 'Alarm Off')
    currentminute = 4
    
if int(currenthour) == int(morningh):
  if int(currentminute) == int(morningm):
    print('dayalarm')  ###where alarm goes
    LCD1602.write(5, 0, '%s:%s' % (currenthour,currentminute))
    LCD1602.write(2, 1, 'Wake Up')
    buzzsetup()
    buzzloop()
    if GPIO.input(buttonPin) == 1:
      buzzdestroy()
      LCD1602.write(0, 1, 'Alarm Off')