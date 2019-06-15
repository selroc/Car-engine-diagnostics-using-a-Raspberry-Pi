"""@package ADC

This is the analogue to digital conversion library that is use dto read the signal from a car
"""
#1/usr/bin/env python
#program to read analogue voltage on Custard Pi 2
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT) #pin26 is chip select 1
GPIO.setup(23, GPIO.OUT) #pin23 is clock
GPIO.setup(19, GPIO.OUT) #pin19 is data out
GPIO.setup(24, GPIO.OUT) #pin24 is chip select 0
GPIO.setup(21, GPIO.IN) #pin21 is data in 
#set pins to default state
GPIO.output(24, True)
GPIO.output(26, True)
GPIO.output(23, False)
GPIO.output(19, True)
#set up data for ADC chip
word5= [1, 1, 0, 1, 1]
word6= [1, 1, 1, 1, 1]

def readchannel0():
    #reads analogue voltge from channel 0
    GPIO.output(24, False) #select channel 0
    anip=0 #initialise variable
    #set up channel 0
    for x in range (0,5):
        GPIO.output(19, word5[x])
        #time.sleep(0.01)
        GPIO.output(23, True)
        #time.sleep(0.01)
        GPIO.output(23, False)

    #read analogue voltage
    for x in range (0,12):
        GPIO.output(23,True)
        #time.sleep(0.01)
        bit=GPIO.input(21)
        #time.sleep(0.01)
        GPIO.output(23,False)
        value=bit*2**(12-x-1)
        anip=anip+value

    GPIO.output(24, True)
    volt = anip*3.3/4096
    return volt

def readchannel1():
    #reads analogue voltge from channel 1
    GPIO.output(24, False) #select channel 1
    anip=0 #initialise variable
    #set up channel 1
    for x in range (0,5):
        GPIO.output(19, word6[x])
        time.sleep(0.001)
        GPIO.output(23, True)
        time.sleep(0.001)
        GPIO.output(23, False)
    #read analogue voltage
    for x in range (0,12):
        GPIO.output(23,True)
        time.sleep(0.001)
        bit=GPIO.input(21)
        time.sleep(0.001)
        GPIO.output(23,False)
        value=bit*2**(12-x-1)
        anip=anip+value

    GPIO.output(24, True)
    volt = (anip*3.3)/4096
    return volt 
