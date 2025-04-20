from gpiozero import LED
from time import sleep
import subprocess

#config
led= LED(24)
interval= 5
host_ping="8.8.8.8" #googles public DNS

def is_connected():
    try:
        subprocess.check_call(['ping', '-c', '1', host_ping], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
def indicate():  
    try:
        if is_connected():
            led.on()
            sleep(interval)
            #print("Conected")
        else:
            led.off()
            #print("Not Connected")
    except:
        pass

def cleanup():
    led.close()