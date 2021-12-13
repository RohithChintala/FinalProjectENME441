#!/usr/bin/python37all
from datetime import datetime, timedelta
import json
import pytz
import RPi.GPIO as GPIO
import time
from calendardata import getcalendardata
from LCD1602 import init, write, clear
from custompassiveBuzzer import buzzsetup, buzzloop, buzzdestroy
from custompassiveBuzzer import CL,CM,CH,song_1,song_2,song_3,beat_1,beat_2,beat_3

init(0x27, 1) #initializes LCD1602 location
GPIO.setmode(GPIO.BOARD) #sets gpio mode
buttonPin = 29 #sets button pin to be 29
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #sets button pin to be a pull down
morningh = 0 #sets moningh to initially be 0
morningm = 0 #sets moningm to initially be 0
nighth = 0 #sets nighth to initially be 0
nightm = 0 #sets nightm to initially be 0

while True: #runs continuously
  with open('final.txt', 'r') as f: #opens json dump file
    data = json.load(f) #sets data to be loaded from json dump file
    m = [data['mhours'],data['mmin']] #creats m array from mhours and mmin collected from json (the amount of time to wake up before an event)
    n = [data['nhours'],data['nmin']] #creats n array from nhours and nmin collected from json (amount of sleep to get)
    r = [data['rhours'],data['rmin']] #creats r array from rhours and rmin collected from json (when to refresh reading calendar)
    sound = data['sounds'] #sets sound variable to be from json
  LOCAL_TIMEZONE = "America/New_York"
  timezone = pytz.timezone(LOCAL_TIMEZONE) #sets local timezone
  now = timezone.localize(datetime.now()) #finds current time datat
  currentdayname = now.strftime("%a") #gets current day in letters
  currentyear = now.strftime("%y") #gets current year
  currentday = now.strftime("%d") #gets current day in numbers
  currentmonth = now.strftime("%b") #gets current month
  currenthour = now.strftime("%H") #gets current hour
  currentminute = now.strftime("%M") #gets current minute
  currentsecond = now.strftime("%S") #gets current second
  if sound == 'sound1': #if sound1 is selected in the json 
    song = song_1 #sets song to be song_1
    beat = beat_1 #sets beat to be beat_1
  elif sound == 'sound2': #if sound2 is selected in the json 
    song = song_2 #sets song to be song_2
    beat = beat_2 #sets beat to be beat_1
  elif sound == 'sound3': #if sound2 is selected in the json 
    song = song_3 #sets song to be song_3
    beat = beat_3 #sets beat to be beat_1
  
  write(5, 0, '%s:%s' % (currenthour,currentminute)) #diplays current hour and minute on the LCD display
  write(0, 1, "%s, %s, %s,'%s" % (currentdayname,currentday,currentmonth, currentyear)) #displays currentdays name, current day, current month, current year
  if data['test'] == 'testing': #checks if the radio button for volume testing is checked
    buzzsetup() #initializes buzzer
    for i in range(1, int((len(song)/2)): #runs for half the length of a given zong
      buzzloop(GPIO.input(buttonPin),song[i],beat[i]) #passes buzzloop the current pin value, song value and beat value for an i
    buzzdestroy() #stops the buzzer when the song is done
  if int(currenthour) == int(r[0]): #checks if the current hour is the refresh hour
    if int(currentminute) == int(r[1]): #checks if the current minute is the refresh minute
      if int(currentsecond) == 0: #runs at the start of the minute
        wake = getcalendardata() #gets calendar data 
        morningh = int(wake[0])- int(m[0]) #sets morningh (morningalarms hour) to be the event time minus the desired morning hours
        morningm = int(wake[1])- int(m[1]) #sets morningm (morningalarms minute) to be te event minute minus the desired morning minutes
        if morningm < 0: #if morning m is below 0 
            morningh -= 1 #decreases the morning hours by 1
            morningm = 60 - int(m[1]) #sets minutes to be decreased from 60 to get correct time
        if morningh < 0: #if morninh is less than 0
          morningh = 24 + morningh #decrease morningh from 24 hours
        nighth = morningh - int(n[0]) #sets nighth to be the desired sleeping hours subtracted from the morningh
        nightm = morningm - int(n[1]) #sets night, to be the desired sleeping minutes subtracted from the morning,
        if nightm < 0: #if nightm is less than 0
            nighth -= 1 #decreases nighth by 1
            nightm = 60 - int(n[1]) #sets minutes to be decreased from 60 to get correct time
        if nighth < 0: #if nighth is less than 0
          nighth = 24 + nighth #decrease nighth from 24 hours

  if int(currenthour) == nighth: #checks if current time is equal to night alarms hour
    if int(currentminute) == nightm: #checks if current minute is equal to night alarms minute
      if int(currentsecond) == 0: #runs once at the start of the minute
        clear() #clears the LCD display
        write(5, 0, '%s:%s' % (currenthour,currentminute)) #writes the current hour and minute
        write(2, 1, 'Time To Sleep') #writes time to sleep on the dislpay
        buzzsetup() #sets up buzzer
        g = 0 #sets variable g to initially be 0
        while GPIO.input(buttonPin) < 1: #runs while button is not pressed
          buzzloop(GPIO.input(buttonPin),song[g],beat[g]) #passes buttonvalue, song and beat for a given g to buzzer
          g += 1 #increases g by 1
          if g == len(song): #if g is equal to the length of the song resets it to 0 to play the song on a loop
            g = 0
        buzzdestroy()#stops the buzzer
        clear() #clears display
        write(2, 1, 'Alarm Off') #writes alarm off on the display
        time.sleep(1) #sleeps for 1 second
        clear() #clears the display
  if int(currenthour) == morningh: #runs if the current hour is equalt to the hour of the morning alarm
    if int(currentminute) == morningm: #runs if the current minute is equal to the minute of the morning alarm
      if int(currentsecond) == 0: #runs once at the start of the minute
        snooze = int(data['snooze']) #sets snooze to be the amount of snoozes desired from the json
        for s in range(snooze+1): #runs for the amount of snoozes + 1 to include the original alarm iteration
          clear() #clears lcd
          write(5, 0, '%s:%s' % (currenthour,currentminute)) #writes the current time
          write(2, 1, 'Wake Up') #writes wakeup on the LCD
          buzzsetup() #sets up the buzzer
          g = 0 #sets variable g to originally be 0
          while GPIO.input(buttonPin) < 1: #runs while the button is not pressed
            buzzloop(GPIO.input(buttonPin),song[g],beat[g]) #passes button value, song and beat for g
            g+=1 #increases g by 1
            if g == len(song): #if g equals the length of the song, resets g to 0
              g = 0
          buzzdestroy() #stops the buzzer once the button is pressed

          if s < snooze: #checks if the current s is less than the amount of snoozes
            clear() #clears lcd 
            write(2, 1, 'Alarm Snooze') #writes alarm snooze on LCD
            for g in range(30): #runs 30 times
              time.sleep(1) #sleeps for 1 second
              now = timezone.localize(datetime.now()) #collects current time
              currenthour = now.strftime("%H") #gets current hour from now
              currentminute = now.strftime("%M") #gets current minute from now
              write(5, 0, '%s:%s' % (currenthour,currentminute)) #writes the current time to the LCD
        clear() #clears the LCD
        write(2, 1, 'Alarm Off') #writes alarm off on the LCD
        time.sleep(1) #sleeps for 1 seconds
        clear() #clears the LCD
