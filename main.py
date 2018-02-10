from machine import I2C, Pin
import time
import ujson

# CONSTANTS
SLAVE_ADDRESS = 0x39

i2cport =I2C(scl=Pin(5), sda=Pin(4), freq=100000)
i2cport.writeto_mem(SLAVE_ADDRESS, 0, b'\0x03')

lux_sensor = {'channel_0': 0, 'channel_1' : 0}
lux_input = [201]
iterator = 0;

def process_input_data():
    data0low = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8C,1),'big')
    data0high = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8D,1),'big')

    data1low = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8E,1),'big')
    data1lhigh = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8F,1),'big')

    channel0 = data0high*256 + data0low
    channel1 = data1lhigh*256 + data1low

    lux_sensor['channel_0'] = channel0
    lux_sensor['channel_1'] = channel1
    return;


while(True):
#    pin.on() #LED ON
    if (iterator >= 200):
        for i in lux_input:
            print(i)
        iterator = 0;

    iterator = iterator + 1;

    process_input_data()

    lux_input.append(lux_sensor['channel_0'])


    print(ujson.dumps(lux_sensor))

    time.sleep(0.2)

#    pin.off() #LED OFF

#i2cport.writeto_mem(57, 0x00, bytearray([0x03]))
