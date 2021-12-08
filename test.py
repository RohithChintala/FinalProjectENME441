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
from custompassiveBuzzer import buzzsetup, buzzloop, buzzdestroy
GPIO.setmode(GPIO.BOARD)

buttonPin = 29
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
currenthour = 1
nighth = 1
currentminute = 1
nightm = 1

morningh = 2
morningm = 2

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes
song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3],
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]

LCD1602.init(0x27, 1)
while True:
  if int(currenthour) == int(nighth):
    if int(currentminute) == int(nightm):
      print(GPIO.input(buttonPin)) ###where alarm goes
      LCD1602.write(5, 0, '%s:%s' % (currenthour,currentminute))
      LCD1602.write(2, 1, 'Time To Sleep')
      buzzsetup()
      for i in range(1, len(song_1)):
        buzzloop(GPIO.input(buttonPin),song_1[i])
      #if GPIO.input(buttonPin) == 0:
      # buzzdestroy()
      # LCD1602.write(0, 1, 'Alarm Off')
      currentminute = 4
      LCD1602.clear()
      LCD1602.write(2, 1, 'Done')
      
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