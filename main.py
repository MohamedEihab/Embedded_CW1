from machine import I2C, Pin
import time
import utime
import machine
import ujson
import HeartRateProcessor

# CONSTANTS
SLAVE_ADDRESS = 0x39

i2cport_acc = I2C(scl = Pin(2), sda = Pin(16), freq = 100000)
i2cport =I2C(scl=Pin(5), sda=Pin(4), freq=100000)

HeartRateClass = HeartRateProcessor.HeartRateProcessorClass()

i2cport.writeto_mem(SLAVE_ADDRESS, 0, b'\0x03')

#temp setup
i2cport_acc.writeto_mem(24, 0x1F, b'\0xC0')
i2cport_acc.writeto_mem(24, 0x23, b'\0x80')
i2cport_acc.writeto_mem(24, 0x20, bytearray([0x7F]))

#LED Pin

LED_out = machine.Pin(15, machine.Pin.OUT)

lux_sensor = {'channel_0': 0, 'channel_1' : 0}
temp_sensor = {'temperature' : 0}
gyro = {'x_dir' : 0, 'y_dir' : 0, 'z_dir' : 0}

lux_input = [201]
iterator = 0;

def process_input_data():

    #lux sensor data
    data0low = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8C,1),'big')
    data0high = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8D,1),'big')

    data1low = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8E,1),'big')
    data1lhigh = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8F,1),'big')

    channel0 = data0high*256 + data0low
    channel1 = data1lhigh*256 + data1low

    lux_sensor['channel_0'] = channel0
    lux_sensor['channel_1'] = channel1

    #temperature data
  #  temp_low = int.from_bytes(i2cport_acc.readfrom_mem(24,0x0C,1),'big')
  #  temp_high = int.from_bytes(i2cport_acc.readfrom_mem(24,0x0D,1),'big')

  #  temp_sensor['temperature'] = 256*temp_high + temp_low;

    #acceler data
    X_L = i2cport_acc.readfrom_mem(24, 0x28, 1)
    X_H = i2cport_acc.readfrom_mem(24, 0x29, 1)
    Y_L = i2cport_acc.readfrom_mem(24, 0x2A, 1)
    Y_H = i2cport_acc.readfrom_mem(24,0x2B, 1)
    Z_L = i2cport_acc.readfrom_mem(24, 0x2C, 1)
    Z_H = i2cport_acc.readfrom_mem(24,0x2D,1)

    x_comb = int.from_bytes(X_H,'big')
    y_comb = int.from_bytes(Y_H,'big')
    z_comb = int.from_bytes(Z_H,'big')

    gyro['x_dir'] = x_comb;
    gyro['y_dir'] = y_comb;
    gyro['z_dir'] = z_comb;

    return;


while(True):
    process_input_data()
    HeartRateClass.process_raw_lux(lux_sensor['channel_0'])
    #HeartRateProcessor.tick()
    utime.sleep_ms(10) # 20 readings in a second

#i2cport.writeto_mem(57, 0x00, bytearray([0x03]))
