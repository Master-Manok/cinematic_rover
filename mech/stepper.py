from gpiozero import DigitalOutputDevice
from time import sleep

steps_per_rev= 200
speed= 100
microstepping=1

delay_s= 60.0/(steps_per_rev*speed)/microstepping

#xy plane
xy_dir= DigitalOutputDevice(2)
xy_step= DigitalOutputDevice(3)
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

def cleanup():
    xy_dir.close()
    xy_step.close()
    yz_dir.close()
    yz_step.close()