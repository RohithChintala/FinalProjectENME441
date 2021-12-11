#!/usr/bin/python37all
from datetime import datetime, timedelta
import json
import pytz
import RPi.GPIO as GPIO
import time
from calendardata import getcalendardata
from LCD1602 import init, write, clear
from custompassiveBuzzer import buzzsetup, buzzloop, buzzdestroy
from custompassiveBuzzer import CL,CM,CH,song_1,song_2,song_3,song_test,beat_1,beat_2,beat_3,beat_test
'''
CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes

song1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6],
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3],
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]

song_2 = [	CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], 
			CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2],
			CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1],
			CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]	]

song3 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6],
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3],
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]
'''

  #####
  ####ADD Different Songs
  ####
 ####DO RTIME BOOLEAN FOR am pm
 ######
 ######Rewrite all morningh and morningm to be m[0]and m[1]
 ######
 ###Things to do
 ##add testing for volume---------------------
 ##add display of schedule for next day
 ##add different songs
 ##comment out code
 ##add snooze make to json

init(0x27, 1)
GPIO.setmode(GPIO.BOARD)
buttonPin = 29
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True: #runs continuously
  with open('final.txt', 'r') as f: #opens json dump file
    data = json.load(f) #sets data to be loaded from json dump file
    m = [data['mhours'],data['mmin']]
    n = [data['nhours'],data['nmin']]
    r = [data['rhours'],data['rmin']]
    sound = data['sounds']
  LOCAL_TIMEZONE = "America/New_York"
  timezone = pytz.timezone(LOCAL_TIMEZONE)
  now = timezone.localize(datetime.now())
  currentdayname = now.strftime("%a")
  currentday = now.strftime("%d")
  currentmonth = now.strftime("%b")
  currenthour = now.strftime("%H")
  currentminute = now.strftime("%M")
  currentsecond = now.strftime("%S")
  if sound == 'sound1':
    song = song_1
    beat = beat_1
  elif sound == 'sound2':
    song = song_2
    beat = beat_2
  elif sound == 'sound3':
    song = song_3
    beat = beat_3
  clear()
  write(5, 0, '%s:%s' % (currenthour,currentminute))
  write(0, 1, '%s, %s, %s' % (currentdayname,currentday,currentmonth))
  if data['test'] == 'testing':
    buzzsetup()
    for i in range(1, len(song)):
      buzzloop(GPIO.input(buttonPin),song[i],beat[i])
    buzzdestroy()
  if int(currenthour) == r[0]:
    if int(currentminute) == r[2]:
  #if int(currenthour) == int(currenthour): 
    #if int(currentminute) == int(currentminute):
      wake, currentday = getcalendardata()
      morningh = int(wake[0])- int(m[0])
      morningm = int(wake[1])- int(m[1])
      if morningm < 0:
          morningh -= 1
          morningm = 60 - m[1]
      if morningh < 0:
        morningh = 24 + morningh
      nighth = morningh - int(n[0])
      nightm = morningm - int(n[1])
      if nightm < 0:
          nighth -= 1
          nightm = 60 - n[1]
      if nighth < 0:
        nighth = 24 + nighth
      if int(currenthour) == nighth: #Night Alarm
        if int(currentminute) == nightm:
          if int(currentsecond) == 0:
            clear()
            write(5, 0, '%s:%s' % (currenthour,currentminute))
            write(2, 1, 'Time To Sleep')
            buzzsetup()
            for i in range(1, len(song)):
              buzzloop(GPIO.input(buttonPin),song[i])
            clear()
            write(2, 1, 'Alarm Off')
      if int(currenthour) == morningh: #Day Alarm
        if int(currentminute) == morningm:
          if int(currentsecond) == 0:
            snooze = int(data['snooze'])
            for s in range(snooze+1):
              clear()
              write(5, 0, '%s:%s' % (currenthour,currentminute))
              write(2, 1, 'Wake Up')
              buzzsetup()
              for i in range(1, len(song)):
                buzzloop(GPIO.input(buttonPin),song[i])
              if s < snooze:
                clear()
                write(2, 1, 'Alarm Snooze')
                for g in range(5):
                  time.sleep(1)
                  now = timezone.localize(datetime.now())
                  currenthour = now.strftime("%H")
                  currentminute = now.strftime("%M")
                  write(5, 0, '%s:%s' % (currenthour,currentminute))
            clear()
            write(2, 1, 'Alarm Off')
