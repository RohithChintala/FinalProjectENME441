#!/usr/bin/env python3
#---------------------------------------------------
#
#	This is a program for Passive Buzzer Module
#		It will play simple songs.
#	You could try to make songs by youselves!
#
#		Passive buzzer 			   Pi
#			VCC ----------------- 3.3V
#			GND ------------------ GND
#			SIG ---------------- Pin 11
#
#---------------------------------------------------

import RPi.GPIO as GPIO
import time
import random
Buzzer = 11

CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes

song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3],
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]

beat_1 = [	1, 1, 3, 1, 1, 3, 1, 1, 			# Beats of song 1, 1 means 1/8 beats
			1, 1, 1, 1, 1, 1, 3, 1,
			1, 3, 1, 1, 1, 1, 1, 1,
			1, 2, 1, 1, 1, 1, 1, 1,
			1, 1, 3	]

song_2 = [	CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
			CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2],
			CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1],
			CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]	]

beat_2 = [	1, 1, 2, 2, 1, 1, 2, 2, 			# Beats of song 2, 1 means 1/8 beats
			1, 1, 2, 2, 1, 1, 3, 1,
			1, 2, 2, 1, 1, 2, 2, 1,
			1, 2, 2, 1, 1, 3 ]

notes = {"B0": 31,"C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46,"G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,"C2": 65,"CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,"G2": 98,"GS2": 104,"A2": 110,"AS2": 117,"B2": 123,"C3": 131,"CS3": 139,"D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185,"G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,"C4": 262,"CS4": 277,"D4": 294,"DS4": 311,"E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,"E5": 659,"F5": 698,"FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1319,"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661,"A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520,"AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978}    

mario = ["E4","E4","E4",
"C4","E4","G4","G3",
"C4","G3","E3",
"A3","B3","B3", "A3",
"G3", "E4","G4","A4",
"F4","G4","E4","C4","D4","B3",
"C4","G3","E3",
"A3","B3","B3","A3",
"G3","E4","G4","A4",
"F4","G4","E4","C4","D4","B3",
"G4","FS4","F4","D4","E4",
"G3","A3","C4",
"A3","C4","D4",
"G4","FS4","F4","D4","E4",
"C5","C5","C5"
"G4","FS4","F4","D4","E4",
"G3","A3","C4",
"A3","C4","D4",
"DS4","D4","C4",
"C4","C4","C4",
"C4","D4","E4","C4","A3","G3",
"C4","C4","C4",
"C4","D4","E4",
"C4","C4","C4",
"C4","D4","E4","C4","A3","G3",
"E4","E4","E4",
"C4","E4","G4",
"G3",
"C4","G3","E3",
"A3","B3","B3","A3",
"G3","E4","G4","A4",
"F4","G4","E4","C4","D4","B3",
"C4","G3","E3",
"A3","B3","B3","A3",
"G3","E4","G4","A4",
"F4","G4","E4","C4","D4","B3",
"E4","C4","G3",
"G3","A3","F4","F4","A3",
"B3","A4","A4","A4","G4","F4",
"E4","C4","A3","G3",
"E4","C4","G3",
"G3","A3","F4","F4","A3",
"B3","F4","F4","F4","E4","D4","C4",
"G3","E3","C3",
"C4","G3","E3",
"A3","B3","A3",
"GS3","B3","GS3",
"G3","FS3","G3"
]


beat_3=[0]*len(mario)
song_3=[0]*len(mario)
for i in range(186):
  song_3[i] = notes[mario[i]]
  beat_3[i]=random.randint(1,2)

song_test = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], CM[5], CM[2]]

beat_test = [	1, 1, 2, 2, 1, 1, 2, 2,
			1, 1, 2, 2, 1, 1, 3, 1 ]


def buzzsetup():
	GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
	GPIO.setup(Buzzer, GPIO.OUT)	# Set pins' mode is output
	global Buzz						# Assign a global variable to replace GPIO.PWM
	Buzz = GPIO.PWM(Buzzer, 440)	# 440 is initial frequency.
	Buzz.start(50)					# Start Buzzer pin with 50% duty ration

def buzzdestroy():
	Buzz.stop()					# Stop the buzzer
	GPIO.output(Buzzer, 1)		# Set Buzzer pin to High
	#GPIO.cleanup()				# Release resource


def buzzloop(pin,song,beat):
  if pin == 0:
    Buzz.ChangeFrequency(int(song))	# Change the frequency along the song note
    #time.sleep(.5)
    time.sleep(beat*0.25)
  if pin == 1:
    buzzdestroy()

      #time.sleep(beat_1[i] * 0.25)		# delay a note for beat * 0.5s
   # elif pin == 1:
    #  buzzdestroy()




'''
if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()

'''