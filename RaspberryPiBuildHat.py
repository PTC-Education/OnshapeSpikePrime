from OnshapePlus import *
from buildhat import Motor

##
##
## Config Client
try:
    try:
        exec(open('../apikeys.py').read())
        try:
            print("Base URL defined as " + base)
        except:
            print("Base URL not specified, defaulting to https://cad.onshape.com")
            base = 'https://cad.onshape.com'
        client = Client(configuration={"base_url": base,
                                    "access_key": access,
                                    "secret_key": secret})
        print('client configured')
    except:
        exec(open('apikeys.py').read())
        base = 'https://cad.onshape.com'
        client = Client(configuration={"base_url": base,
                                    "access_key": access,
                                    "secret_key": secret})
        print('client configured')
except:
    print("apikeys file not found, please enter them manually.")
    access = input('Please enter your access key: ')
    secret = input('Please enter your secret key: ')
    base = input('Please enter your base URL (e.g. "https://cad.onshape.com"): ')
    client = Client(configuration={"base_url": base,
                                "access_key": access,
                                "secret_key": secret})
    print('client configured')

url = str(input('What is the url of your Onshape assembly? (paste URL then press enter twice): '))

## Bug - url input does not continue after copy paste. placeholder fix for now
placeholder = input()

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

defaultPorts = input('Is your motor in port A? [y/n]: ')
if defaultPorts == "y":
    motor = Motor('A')
    motor.when_rotated = handle_motor
    motor.set_default_speed(50)
    # sensor1Port = 'B'
else:
    motor1Port = input('What port is the motor in? ')
    # sensor1Port = input('What port is the sensor in? ')

controlMode = input('Would you like your assembly mate to control the speed or position of the motor? [speed/position]: ')

defaultMates = input('Do you have a mate in your assembly named "Control"? [y/n]: ')
if defaultMates == "y":
    controlMate = 'Control'
    monitorMate = 'Monitor'
else:
    controlMate = input('What is the name of the mate you want to control?')
    # monitorMate = input('What is the name of the mate you want to use as a monitor?')

mates = getMates(client,url,base)
for names in mates['mateValues']:
    print(names['mateName'])

# controlMate = input('What is the name of the mate you want to control your Spike with? ')
# monitorMate = input('What mate do you want the Spike to control? ')

try:
    while True:
        mates = getMates(client,url,base)
        for names in mates['mateValues']:
            if names['mateName'] == controlMate:
                if names['jsonType'] == "Revolute":
                    pos = math.floor(translate(names['rotationZ'],0,math.pi,180,0))
                    speed = math.floor(translate(names['rotationZ'],0,2*math.pi,0,255))
                elif names['jsonType'] == "Slider":
                    pos = math.floor(translate(names['translationZ'],0,math.pi,180,0))
                    speed = math.floor(translate(names['translationZ'],0,2*math.pi,0,100))
        if controlMode == "position":
            print('Control pos = '+str(pos))
            posControl(pos)
        elif controlMode == "speed":
            print('Control speed = '+str(speed))
            speedControl(speed)
        time.sleep(1)
except KeyboardInterrupt:
    motor.stop()
    print('done')