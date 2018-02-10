from machine import I2C, Pin
import time

i2cport =I2C(scl=Pin(5), sda=Pin(4), freq=100000)
i2cport.writeto_mem(57, 0, b'\0x03')


while(True):
#    pin.on() #LED ON

    data0low = int.from_bytes(i2cport.readfrom_mem(57,0xC,1),'big')
    data0high = int.from_bytes(i2cport.readfrom_mem(57,0xD,1),'big')
    channel0 = data0high*256 + data0low
    data1low = i2cport.readfrom_mem(57,0xE,1)
    data1lhigh = i2cport.readfrom_mem(57,0xF,1)

    print("%d; %d; %d; %d", data0low,data0high,data1low,data1lhigh)
    print(channel0)
    time.sleep(0.2)

#    pin.off() #LED OFF

i2cport.writeto_mem(57, 0x00, bytearray([0x03]))
