#!/usr/bin/python37all

import RPi.GPIO as GPIO
import time
import json

ledPin1 = 19
ledPin2 = 17
ledPin3 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

pwm1 = GPIO.PWM(ledPin1, 100) # PWM object on our pin at 100 Hz
pwm1.start(0) # start with LED 1 off
pwm2 = GPIO.PWM(ledPin2, 100) # PWM object on our pin at 100 Hz
pwm2.start(0) # start with LED 2 off
pwm3 = GPIO.PWM(ledPin3, 100) # PWM object on our pin at 100 Hz
pwm3.start(0) # start with LED 3 off

while True: #runs continuously
  with open('final.txt', 'r') as f: #opens json dump file
    data = json.load(f) #sets data to be loaded from json dump file
    dutyCycle = float(data['slider1'])  #sets duty cycle to be a float from data
  if data['Le'] == '1': #runs if LED 1 is selected in radio button
    pwm1.ChangeDutyCycle(dutyCycle) #changes duty cycle for LED 1
    time.sleep(0.1) #sleeps for .1 seconds
  if data['Le'] == '2':  #runs if LED 2 is selected in radio button
    pwm2.ChangeDutyCycle(dutyCycle) #changes duty cycle for LED 2
    time.sleep(0.1) #sleeps for .1 seconds
  if data['Le'] == '3':  #runs if LED 3 is selected in radio button
    pwm3.ChangeDutyCycle(dutyCycle) #changes duty cycle for LED 3
    time.sleep(0.1) #sleeps for .1 seconds
