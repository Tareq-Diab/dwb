#!/usr/bin/env python
import time 
import RPi.GPIO as GPIO
from read_RPM import reader
import pigpio


class motorspeed:
    def __init__(self,pin,resolution):
        self.pi=pigpio.pi()
        self.resolution=resolution
        self.motor=reader(self.pi,pin,resolution)
        self.prev=0
        self.counter=0
    def RPS(self):
        self.F=self.motor.frequency()
        #self.motor._high=None
        #self.motor._high_tick=None
        #self.motor._period=None
        
        if self.F == self.prev :
            return 0
        else :
            
            return self.F/self.resolution
            
    def RPM(self):
        self.rpm=self.motor.RPM()
        return self.rpm

"""
GPIO.setmode(GPIO.BOARD)
pi = pigpio.pi()
ml=reader(pi,5)

while 1 :
    try:
        time.sleep(0.1)
        print(ml.frequency())
        ml._high=None
        ml._high_tick=None
        ml._period=None
    except:
        print("error occured")
        pass
"""
