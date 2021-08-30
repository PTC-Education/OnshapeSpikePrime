import time
import math
import serial
import sys
import glob
import json

from onshape_client.client import Client
from onshape_client.onshape_url import OnshapeElement

## Define Serial Functions for connecting to Spike
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
        for port in ports:
            if 'usb' in port:
                guess = port                
                
        try:
            return guess
        except:
            print('no USB ports found')
            quit()
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return ports

def serial_write(string):
    ser.write(string + b'\r\n')
    time.sleep(0.1)
    while ser.in_waiting:  
        print(ser.read(ser.in_waiting).decode())

## Initialize connection to Spike
port = serial_ports()

try:
    ser = serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
except:
    serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    ).close()
    print("Port is closed")
    ser = serial.Serial(
        port=port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    print("Port is open again")

print(ser.isOpen())

## Beep if connected
ser.write(b'\x03')
serial_write(b'import hub')
serial_write(b'hub.sound.beep()')
time.sleep(1)
while ser.in_waiting:  
    ser.read(ser.in_waiting)

##
##
## Config Onshape Client
exec(open('../../Documents/colabkeys.py').read())
base = 'https://cad.onshape.com'
client = Client(configuration={"base_url": base,
                               "access_key": access,
                               "secret_key": secret})
print('client configured')

url = input('what is the assembly url? ')
## Get Mates Function
def getMates():
  fixed_url = '/api/assemblies/d/did/w/wid/e/eid/matevalues'
  element = OnshapeElement(url)
  method = 'GET'

  params = {}
  payload = {}
  headers = {'Accept': 'application/vnd.onshape.v2+json',
              'Content-Type': 'application/vnd.onshape.v2+json'}

  fixed_url = fixed_url.replace('did', element.did)
  fixed_url = fixed_url.replace('wid', element.wvmid)
  fixed_url = fixed_url.replace('eid', element.eid)

  response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers, body=payload)

  parsed = json.loads(response.data)
  # The command below prints the entire JSON response from Onshape
  # print(json.dumps(parsed, indent=4, sort_keys=True))
  return parsed

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

while True:
  pos = str(math.floor(translate(getMates()['mateValues'][0]['rotationZ'],0,math.pi,180,0)))
  string = 'hub.port.D.motor.run_to_position('+pos+',speed=20)'
  serial_write(string.encode())
  time.sleep(2)

