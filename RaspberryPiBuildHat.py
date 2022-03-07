## Import custom Onshape library of functions
from turtle import distance
from OnshapePlus import *
## Import any necessary libraries for buildhat
from buildhat import Motor, DistanceSensor


##
## Config API Client
##

## Best practice is to add you API keys and base URL to a separate file named "apikeys.py" in the folder
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

## If keys are not in separate file, you can input them directly here, but make sure you never share this file
except:
    access = "<access key>"
    secret = "<secret key>"
    base = "https://cad.onshape.com" ## Change base url if working in an enterprise
    client = Client(configuration={"base_url": base,
                                "access_key": access,
                                "secret_key": secret})
    print('client configured')

##
## define buildhat functions and params
##
def handle_motor(speed, pos, apos):
    print("Motor", speed, pos, apos)

def posControl(pos):
    motor.run_to_position(pos)

def speedControl(speed):
    motor.set_default_speed(speed)
    motor.start()

## Chage motor port if different or comment out if not using a motor
motor = Motor('A')
motor.when_rotated = handle_motor
motor.set_default_speed(50)

## Chage sensor port if different and make sure you are using the correct sensor code for buildhat
dist = DistanceSensor('B')


##
## Specify Onshape funcitons and parameters
##

## Change URL to be your Assmelby
url = "https://rogers.onshape.com/documents/a77394b9ba5137d73e469838/w/777a0833ba8f13c86be92c64/e/f211c2e72faad8ab59387b14"

## What is the name of the mate you want to use to control a motor?
controlMate = 'Control'
## What is the name of the mate you want to use to monitor a sensor input?
monitorMate = 'Monitor'

mates = getMates(client,url,base)
for names in mates['mateValues']:
    print(names['mateName'])


try:
    while True:
        ##
        ## The part where you control a motor with an Onshape Assembly Mate
        ##

        ## First get the mate value and map it to the value you really want
        mates = getMates(client,url,base)
        for names in mates['mateValues']:
            if names['mateName'] == controlMate:
                if names['jsonType'] == "Revolute":
                    pos = math.floor(translate(names['rotationZ'],0,math.pi,180,0))
                    speed = math.floor(translate(names['rotationZ'],0,2*math.pi,0,100))
                elif names['jsonType'] == "Slider":
                    pos = math.floor(translate(names['translationZ'],0,2,180,0))
                    speed = math.floor(translate(names['translationZ'],0,2,0,100))
        
        print("getMateValue = "+str(pos))
        ## Send the value to the motor
        posControl(pos)

        ##
        ## The part where you control an Onshape Assembly Mate with a sensor value
        ##

        ## Get sensor value from buildhat
        monitorValue = dist.get_distance()

        ## Look for mate name you want to control and set body of API request
        for names in mates['mateValues']:
            if names['mateName'] == monitorMate:
                setMateJSON = names
                if names['jsonType'] == "Revolute":
                    setMateJSON['rotationZ'] = translate(monitorValue[0],-1024,1024,0,2*math.pi)
                elif names['jsonType'] == "Slider":
                    setMateJSON['translationZ'] = translate(monitorValue[0],-1024,1024,0,1)
        
        print("setMateValue = "+str(setMateJSON))
        ## Send to Onshape
        setMates(client,url,base,{'mateValues':[setMateJSON]})

        time.sleep(1)
except KeyboardInterrupt:
    motor.stop()
    print('done')