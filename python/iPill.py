from servosix import ServoSix
import time

ss = ServoSix()

period = 2

def dispensePill():
    ss.set_servo(1, 0)
    time.sleep(period)
    ss.set_servo(1, 180)
