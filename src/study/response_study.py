#!/usr/bin/env python

#import matplotlib.pyplot as pyplot
#import matplotlib
import numpy as np

import RPi.GPIO as gpio
import time

from frequncy_calculator import motorspeed
import pickle

#outfile=open("src/response_study_output/respone_analysis",'wb')


gpio.setmode(gpio.BOARD)
mr=[37,35,40]
ml=[33,31,38]
for pin in mr:
    gpio.setup(pin,gpio.OUT)
for pin in ml:
    gpio.setup(pin,gpio.OUT)
speed=0
pwm_mr=gpio.PWM(40,50)
pwm_ml=gpio.PWM(38,50)
pwm_mr.start(0)
pwm_ml.start(0)


pwm_mr.ChangeDutyCycle(speed)
pwm_ml.ChangeDutyCycle(speed)

left_motor=motorspeed(16,231)
right_motor=motorspeed(5,231)
def step_function(amplitude):
    log=np.zeros([501,2])
    t=0
    pwm_mr.ChangeDutyCycle(50)
    print("intialising")
    gpio.output(mr[0],1)
    gpio.output(ml[1],1)
    for i in range(501):
        rps=right_motor.RPM()
        log[i]=[rps,t]
        time.sleep(0.01)
        t=t+0.01
    pwm_mr.ChangeDutyCycle(0)
    gpio.output(mr[0],0)
    pickle.dump(log,outfile)
    outfile.close()
    #plotting the step function response
    """
    fig , ax =plt.subplots()
    ax.plot(log[:,0],log[:,1])
    ax.set(xlable='time (ms)',ylable='rps',title='step function response')
    ax.grid()
    fig.savefig("response_study_output/step_response.png")
    plt.show()
    """

def DutyCycle_rps_relation():
    outfile=open("response_study_output/respone_analysis_DC_RPS",'wb')

    log=np.zeros([101,2])
    gpio.output(mr[0],1)
    gpio.output(ml[1],1)
    for i in range(101):
            pwm_mr.ChangeDutyCycle(i)
            pwm_ml.ChangeDutyCycle(i)
            time.sleep(0.3)
            rps=right_motor.RPM()
            rps_L=left_motor.RPM()
            print(rps,"    ",rps_L)
            log[i]=[rps,i]

    pwm_mr.ChangeDutyCycle(0)
    pwm_ml.ChangeDutyCycle(0)
    gpio.output(mr[0],0)
    #plotting the step function response
    pickle.dump(log,outfile)
    outfile.close()
    """
    fig , ax =plt.subplots()
    ax.plot(log[:,0],log[:,1])
    ax.set(xlable='rps',ylable='Duty Cycle(%)',title='Duty Cycle RPS relation')
    ax.grid()
    fig.savefig("response_study_output/step_response.png")
    plt.show()
    """
if __name__=="__main__":
    DutyCycle_rps_relation()
