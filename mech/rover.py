from gpiozero import Motor
from time import sleep

Left= Motor(forward=26, backward=19)
Right= Motor(forward=13, backward=6)

def mov_for():
    Left.forward()
    Right.forward()
    sleep(1)

def mov_rgt():
    Left.backward()
    Right.forward()
    sleep(1)

def mov_lft():
    Left.forward()
    Right.backward()
    sleep(1)

def mov_bck():
    Left.backward()
    Right.backward()
    sleep(1)

def stop():
    Left.stop()
    Right.stop()

def cleanup():
    Left.close()
    Right.close()
