from gpiozero import DigitalOutputDevice
from time import sleep
import pygame

steps_per_rev= 200
speed= 100
microstepping=1

delay_s= 60.0/(steps_per_rev*speed)/microstepping

#xy plane
xy_dir= DigitalOutputDevice(17)
xy_step= DigitalOutputDevice(27)
#yz plane
yz_dir= DigitalOutputDevice(14)
yz_step= DigitalOutputDevice(15)

def rot_xy(steps, direction):
    xy_dir.value=direction
    for _ in range(steps):
        xy_step.on()
        sleep(delay_s)
        xy_step.off()
        sleep(delay_s)

def rot_yz(steps, direction):
    yz_dir.value=direction
    for _ in range(steps):
        yz_step.on()
        sleep(delay_s)
        yz_step.off()
        sleep(delay_s)

def rot(button,state):
    if(button == 0 and state):
        rot_yz(5,True)
    elif(button == 2 and state):
        rot_yz(5,False)
    elif(button == 3 and state):
        rot_xy(5,True)
    elif(button == 1 and state):
        rot_xy(5,False)
    else:
        xy_dir.off()
        xy_step.off()
        yz_dir.off()
        yz_step.off()

def cleanup():
    xy_dir.close()
    xy_step.close()
    yz_dir.close()
    yz_step.close()