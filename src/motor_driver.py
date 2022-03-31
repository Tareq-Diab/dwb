#!/usr/bin/env python
import RPi.GPIO as gpio
import time
import pygame
from pygame.locals import *

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist 
from frequncy_calculator import motorspeed
gpio.setmode(gpio.BOARD)
mr=[37,35,40]
ml=[33,31,38]
for pin in mr:
    gpio.setup(pin,gpio.OUT)
for pin in ml:
    gpio.setup(pin,gpio.OUT)
speed=50
pwm_mr=gpio.PWM(40,50)
pwm_ml=gpio.PWM(38,50)
pwm_mr.start(0)
pwm_ml.start(0)
v=0.5
z=0.5

pwm_mr.ChangeDutyCycle(0)
pwm_ml.ChangeDutyCycle(0)

rospy.init_node("key_listenser_node")

class motors:
    def __init__(self):
        self.error_l_d=0
        self.error_r_d=0
        self.left_speed=motorspeed(16,231)
        self.right_speed=motorspeed(16,231)
        self.error_l_tprev=0
        self.error_r_tprev=0
        self.kp=0.3
        self.kd=0
        self.ki=0
    def set_rpm(self,l,r):
        if l>0:
            gpio.output(ml[1],1)
            gpio.output(ml[0],0)
        else :
            gpio.output(ml[1],0)
            gpio.output(ml[0],1)
        if r>0:
            gpio.output(mr[1],1)
            gpio.output(mr[0],0)
        else :
            gpio.output(mr[1],0)
            gpio.output(mr[0],1)
        error_l =l-self.left_speed.RPM()
        error_l_d=error_l-self.error_l_tprev
        pwm_l=self.kp*error_l+self.kd*self.error_l_d
        print(pwm_l)
        pwm_l =abs(pwm_l) if abs(pwm_l)<100 else 100
        pwm_ml.ChangeDutyCycle(abs(pwm_l))
        self.error_l_tprev=error_l
        
        
        error_r =r-self.right_speed.RPM()
        error_r_d=error_r-self.error_r_tprev
        pwm_r=self.kp*error_r+self.kd*self.error_r_d 
        pwm_r =abs(pwm_r) if abs(pwm_r)<100 else 100
        pwm_mr.ChangeDutyCycle(abs(pwm_r))
        self.error_r_tprev=error_r   
        
wheel_span=0.275
wheel_circumference=0.082*3.14
motors=motors()
def twis_CB(msg):
    v=msg.linear.x
    w=msg.angular.z
    v_r = ((2 * v) + (w * wheel_span)) / (2 )
    v_l = ((2 * v) - (w * wheel_span)) / (2 )
    w_r=int((v_r/wheel_circumference)*60)
    w_l=int((v_l/wheel_circumference)*60)
    motors.set_rpm(w_l,-w_r)
rospy.Subscriber("cmd_vel", Twist, twis_CB)
while True:
    rospy.spin()
