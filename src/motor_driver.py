#!/usr/bin/env python
import RPi.GPIO as gpio
import time
import pygame
from pygame.locals import *
import math
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist 
from nav_msgs.msg import Odometry
from frequncy_calculator import motorspeed
import tf
import os
os.system("echo 'hakunamatata' | sudo -S pigpiod ")

odom=Odometry()
odom.header.frame_id="odom"
odom.child_frame_id="chassis"
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
theta=0
x=0
y=0
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
odom_publisher=rospy.Publisher("odom",Odometry)
speed_rate=rospy.Rate(50)
while True:
    speed_rate.sleep()
    # //calculating robot speed
    right_speed=motors.right_speed.RPM()*wheel_circumference*(1/60)
    left_speed=motors.left_speed.RPM()*wheel_circumference*(1/60)
    robot_speed=(right_speed+left_speed)/2
    # //calculating change in robot oriantation "YAW"
    dtheta=(right_speed-left_speed)/wheel_span
    # //updating robot orientation "YAW"
    theta=theta+dtheta

    # //robot new position in X
    # //dx is calculated separatly for the twist message
    dx=robot_speed*math.cos(theta)
    x=x+dx
    # //robot new position in y
    # //dy is calculated separatly for the twist message
    dy=robot_speed*math.sin(theta)
    y=y+dy
    quaternion=tf.transformations.quaternion_from_euler(0,0,theta)
    odom.pose.pose.position.x=x
    odom.pose.pose.position.y=y
    odom.pose.pose.position.z=0
    odom.pose.pose.orientation.x=quaternion[0]
    odom.pose.pose.orientation.y=quaternion[1]
    odom.pose.pose.orientation.z=quaternion[2]
    odom.pose.pose.orientation.w=quaternion[3]
    odom.twist.twist.linear.x=dx
    odom.twist.twist.linear.y=dy
    odom.twist.twist.angular.z=dtheta
    odom_publisher.publish(odom)
