#!/usr/bin/python37all
import requests
from datetime import datetime, timedelta
import urllib.parse
import json
import pytz
import RPi.GPIO as GPIO
import time
import json
from calendardata import get_busy_times_from_google_calendar
from LCD1602 import init, write
from passiveBuzzer import buzzsetup, buzzloop, buzzdestroy

init(0x27, 1)
buttonPin = 5
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while True: #runs continuously
  with open('final.txt', 'r') as f: #opens json dump file
    data = json.load(f) #sets data to be loaded from json dump file
    m = [data['mhours'],data['mmin'],data['mtime']]
    n = [data['nhours'],data['nmin'],data['ntime']]
    r = [data['rhours'],data['rmin'],data['rtime']]
  LOCAL_TIMEZONE = "America/New_York"
  timezone = pytz.timezone(LOCAL_TIMEZONE)
  now = timezone.localize(datetime.now())
  currentdayname = now.strftime("%a")
  currentday = now.strftime("%d")
  currentmonth = now.strftime("%b")
  currenthour = now.strftime("%H")
  currentminute = now.strftime("%M")
  #####
  ####
  ####
 ####DO RTIME BOOLEAN FOR am pm
 ######
 ######
 ######3
  write(5, 0, '%s:%s' % (currenthour,currentminute)) #potentially add am
  write(0, 1, '%s, %s, %s' % (currentdayname,currentday,currentmonth))
  if int(currenthour) == r[0]:
    if int(currentminute) == r[2]:
      busy_times, wake, currentday = get_busy_times_from_google_calendar() #delete busy times
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
      #print(nighth, nightm)
      if int(currenthour) == int(n[0]):
        if int(currentminute) == int(n[1]):
          print('nightalarm') ###where alarm goes
          write(5, 0, '%s:%s' % (currenthour,currentminute))
          write(2, 1, 'Time To Sleep')
          buzzsetup()
          buzzloop()
          if GPIO.input(buttonPin) == 1:
            buzzdestroy()
            write(0, 1, 'Alarm Off')
          
      if int(currenthour) == int(m[0]):
        if int(currentminute) == int(m[1]):
          print('dayalarm')  ###where alarm goes
          write(5, 0, '%s:%s' % (currenthour,currentminute))
          write(2, 1, 'Wake Up')
          buzzsetup()
          buzzloop()
          if GPIO.input(buttonPin) == 1:
            buzzdestroy()
            write(0, 1, 'Alarm Off')
