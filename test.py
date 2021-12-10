import requests
from datetime import datetime, timedelta
import urllib.parse
import json
import pytz
import RPi.GPIO as GPIO
import time
import json
from calendardata import get_busy_times_from_google_calendar
from LCD1602 import init, write, clear
from custompassiveBuzzer import buzzsetup, buzzloop, buzzdestroy
GPIO.setmode(GPIO.BOARD)

buttonPin = 29
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
currenthour = 1
nighth = 2
currentminute = 3
nightm = 4

morningh = 5
morningm = 6

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes
song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3],
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5],CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	,CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	,CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	,CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	,CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	,CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	,CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]		]

init(0x27, 1)
while True:
  for i in range(1, len(song_1)):
    buzzloop(GPIO.input(buttonPin),song_1[i])
    if GPIO.input(buttonPin) == 1:
      time.sleep(5)
  clear()
  write(2, 1, 'Alarm Off')
  '''
  if int(currenthour) == int(nighth):
    if int(currentminute) == int(nightm):
      print(GPIO.input(buttonPin)) ###where alarm goes
      write(5, 0, '%s:%s' % (currenthour,currentminute))
      write(2, 1, 'Time To Sleep')
      buzzsetup()
      for i in range(1, len(song_1)):
        buzzloop(GPIO.input(buttonPin),song_1[i])
      #if GPIO.input(buttonPin) == 0:
      # buzzdestroy()
      # LCD1602.write(0, 1, 'Alarm Off')
      currentminute = 4
      clear()
      write(2, 1, 'Done')
      
  if int(currenthour) == int(morningh):
    if int(currentminute) == int(morningm):
      print('dayalarm')  ###where alarm goes
      LCD1602.write(5, 0, '%s:%s' % (currenthour,currentminute))
      LCD1602.write(2, 1, 'Wake Up')
      buzzsetup()
      buzzloop()
      if GPIO.input(buttonPin) == 1:
        buzzdestroy()
        write(0, 1, 'Alarm Off')
  LOCAL_TIMEZONE = "America/New_York"
  timezone = pytz.timezone(LOCAL_TIMEZONE)
  now = timezone.localize(datetime.now())
  currentdayname = now.strftime("%a")
  currentday = now.strftime("%d")
  currentmonth = now.strftime("%b")
  currenthour = now.strftime("%H")
  currentminute = now.strftime("%M")
  write(5, 0, '%s:%s' % (currenthour,currentminute)) #potentially add am
  write(0, 1, '%s, %s, %s' % (currentdayname,currentday,currentmonth))

  '''