from machine import I2C, Pin
import time
import machine
import network
import ujson

pin = machine.Pin(2, machine.Pin.OUT) #Playing around with LEDs and machine pins

i2cport =I2C(scl=Pin(5), sda=Pin(4), freq=100000)
i2cport.writeto_mem(24, 0x20, bytearray([0x7F]))

gyro = {'x_dir' : 0, 'y_dir' : 0, 'z_dir' : 0}

while(True):
    pin.on() #LED ON


    X_L = i2cport.readfrom_mem(24, 0x28, 1)
    X_H = i2cport.readfrom_mem(24, 0x29, 1)
    Y_L = i2cport.readfrom_mem(24, 0x2A, 1)
    Y_H = i2cport.readfrom_mem(24,0x2B, 1)
    Z_L = i2cport.readfrom_mem(24, 0x2C, 1)
    Z_H = i2cport.readfrom_mem(24,0x2D,1)

    x_comb = int.from_bytes(X_H,'big')
    y_comb = int.from_bytes(Y_H,'big')
    z_comb = int.from_bytes(Z_H,'big')

    gyro['x_dir'] = x_comb;
    gyro['y_dir'] = y_comb;
    gyro['z_dir'] = z_comb;

    #print('%d %d %d - TEST2'%(gyro['x_dir'],gyro['y_dir'],gyro['z_dir']))
    print(ujson.dumps(gyro))

    time.sleep(0.2)

    pin.off() #LED OFF

