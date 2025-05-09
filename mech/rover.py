from gpiozero import Motor
from time import sleep

Left= Motor(forward=26, backward=19)
Right= Motor(forward=13, backward=6)
sleep_time= 0.1

def mov_for():
    Left.forward()
    Right.forward()
    sleep(sleep_time)

def mov_rgt():
    Left.backward()
    Right.forward()
    sleep(sleep_time)

def mov_lft():
    Left.forward()
    Right.backward()
    sleep(sleep_time)

def mov_bck():
    Left.backward()
    Right.backward()
    sleep(sleep_time)

def stop():
    Left.stop()
    Right.stop()

def moment(axis,val):
    if (axis == 0 and val>0.99):
        stop()
        mov_rgt()
    elif (axis == 0 and val<-0.99):
        stop()
        mov_lft()
    elif (axis == 1 and val>0.99):
        stop()
        mov_for()
    elif (axis == 1 and val<-0.99):
        stop()
        mov_bck()
    else:
        stop()

def cleanup():
    Left.close()
    Right.close()
