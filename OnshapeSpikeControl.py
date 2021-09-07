from OnshapePlus import *

## Initialize connection to Spike
port = serial_ports()


def serial_write(string):
    ser.write(string + b'\r\n')
    time.sleep(0.1)
    while ser.in_waiting:  
        print(ser.read(ser.in_waiting).decode())

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
## Config Client
exec(open('../../colabkeys.py').read())
base = 'https://cad.onshape.com'
client = Client(configuration={"base_url": base,
                            "access_key": access,
                            "secret_key": secret})
print('client configured')

url = input('What is the url of your Onshape assembly? ')

mates = getMates(client,url,base)
for names in mates['mateValues']:
    print(names['mateName'])

# controlMate = input('What is the name of the mate you want to control your Spike with? ')
# monitorMate = input('What mate do you want the Spike to control? ')

while True:
  mates = getMates(client,url,base)
  for names in mates['mateValues']:
    if names['mateName'] == "Control":
        if names['jsonType'] == "Revolute":
            pos = str(math.floor(translate(names['rotationZ'],0,math.pi,180,0)))
        elif names['jsonType'] == "Slider":
            pos = str(math.floor(translate(names['translationZ'],0,math.pi,180,0)))

  string = 'hub.port.D.motor.run_to_position('+pos+',speed=20)'
  serial_write(string.encode())
  time.sleep(2)