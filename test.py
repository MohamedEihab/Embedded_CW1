from machine import I2C, Pin
import time

i2cport =I2C(scl=Pin(5), sda=Pin(4), freq=100000)
i2cport.writeto_mem(24, 0x20, bytearray([0x7F]))
while(True):

    X_L = i2cport.readfrom_mem(24, 0x28, 1)
    X_H = i2cport.readfrom_mem(24, 0x29, 1)
    Y_L = i2cport.readfrom_mem(24, 0x2A, 1)
    Y_H = i2cport.readfrom_mem(24,0x2B, 1)
    Z_L = i2cport.readfrom_mem(24, 0x2C, 1)
    Z_H = i2cport.readfrom_mem(24,0x2D,1)

    x_comb = int.from_bytes(X_H,'big')
    y_comb = int.from_bytes(Y_H,'big')
    z_comb = int.from_bytes(Z_H,'big')

    print('%d %d %d'%(x_comb,y_comb,z_comb))
    time.sleep(0.2)
