from buildhat import Motor
from OnshapePlus import *

##
##
##
## define buildhat functions
def handle_motor(speed, pos, apos):
    print("Motor", speed, pos, apos)

def posControl(pos):
    motor.run_to_position(pos)

def speedControl(speed):
    motor.set_default_speed(speed)
    motor.start()

motor = Motor('A')
motor.when_rotated = handle_motor
motor.set_default_speed(50)

posControl(100)
time.sleep(2)
posControl(0)
time.sleep(2)