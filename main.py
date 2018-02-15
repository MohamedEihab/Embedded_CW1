from machine import I2C, Pin
import time
import utime
import machine
import ujson
import HeartRateProcessor
import PedometerClass
import MQTTClientClass
import ustruct


# CONSTANTS
SLAVE_ADDRESS = 0x39
TWOG = 16380
Stop = False

i2cport_acc = I2C(scl = Pin(2), sda = Pin(16), freq = 100000)
i2cport =I2C(scl=Pin(5), sda=Pin(4), freq=100000)

i2cport.writeto_mem(SLAVE_ADDRESS, 0, b'\0x03')

#temp setup
i2cport_acc.writeto_mem(24, 0x1F, b'\0xC0')
i2cport_acc.writeto_mem(24, 0x23, b'\0x80')
i2cport_acc.writeto_mem(24, 0x20, bytearray([0x4F]))

#LED Pin

LED_out = machine.Pin(15, machine.Pin.OUT)

lux_sensor = {'channel_0': 0, 'channel_1' : 0}
temp_sensor = {'temperature' : 0}
gyro = {'x_dir' : 0, 'y_dir' : 0, 'z_dir' : 0}

broker_package = {'Steps_Taken' : 0, 'Heart_Rate' : 0}

lux_input = [201]
iterator = 0


def to_signed(x):
    xor_bits = 0xFFFF
    if x>=0x7FFF:
        y = x ^ xor_bits
        y=0-(y+1)
    else: 
        y=x
    return y


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

  #  temp_sensor['temperature'] = 256*temp_high + temp_low

    #acceler data
    X_L = i2cport_acc.readfrom_mem(24, 0x28, 1)
    X_H = i2cport_acc.readfrom_mem(24, 0x29, 1)
    Y_L = i2cport_acc.readfrom_mem(24, 0x2A, 1)
    Y_H = i2cport_acc.readfrom_mem(24,0x2B, 1)
    Z_L = i2cport_acc.readfrom_mem(24, 0x2C, 1)
    Z_H = i2cport_acc.readfrom_mem(24,0x2D,1)

    x_comb = int.from_bytes(X_H,'big')<<8
    y_comb = int.from_bytes(Y_H,'big')<<8
    z_comb = int.from_bytes(Z_H,'big')<<8
    x_combf = float(to_signed(x_comb))
    y_combf = float(to_signed(y_comb))
    z_combf = float(to_signed(z_comb))
    x_combf = x_combf*10/TWOG #Convert to m/s^2
    y_combf = y_combf*10/TWOG
    z_combf = z_combf*10/TWOG

    gyro['x_dir'] = x_combf
    gyro['y_dir'] = y_combf
    gyro['z_dir'] = z_combf

    return

counter = 0;
time = 0;
delay = 20 #delay in ms
simulated_bpm = 70
duty_time = (60/simulated_bpm)/2
duty_counter = duty_time / (delay/1000)
led_switch = 0;
buffered_val = simulated_bpm

HeartRateClass = HeartRateProcessor.HeartRateProcessorClass(delay, buffered_val)
PedometerInstance= PedometerClass.PedometerClass()
#MQTTClientInstance = MQTTClientClass.MQTTClientClass()

while(True):
   # print(ujson.dumps(lux_sensor['channel_0']), ujson.dumps(lux_sensor['channel_1']))
    process_input_data()
    HeartRateClass.process_raw_lux(lux_sensor['channel_1'])
    PedometerInstance.process_raw_data(gyro['x_dir'], gyro['y_dir'], gyro['z_dir'])

    broker_package['Steps_Taken'] = PedometerInstance.getSteps()
    broker_package['Heart_Rate'] = HeartRateClass.getHeartRate()
    #MQTTClientInstance.publish_data('topic/state', bytes(ujson.dumps(broker_package), 'utf-8'));
   # print(bytes(ujson.dumps(broker_package), 'utf-8'))
   # print(ujson.dumps(broker_package))
    #PedometerInstance.process_raw_data(gyro['x_dir'], gyro['y_dir'], gyro['z_dir'])
    #print(ujson.dumps(gyro))
    #HeartRateProcessor.tick()

    if (counter < duty_counter):
        counter += 1;

    else:
        counter = 0;
        if (led_switch == 0):
            led_switch = 1;
            LED_out.on()
        else:
            led_switch = 0;
            LED_out.off()


   # print(counter, duty_counter, duty_time, led_switch)
    utime.sleep_ms(delay) # 20 readings in a second
    time += delay

    if (time % 1000 == 0):
        print("Steps Taken:", PedometerInstance.getSteps())
        
        if (time % 5000 == 0):
            print("Elapsed Time: ", time/1000)

    #print(PedometerInstance.getSteps())
    #print(ujson.dumps(gyro))
    #HeartRateProcessor.tick()
    #utime.sleep_ms(20) # 20 readings in a second
    #Stop = PedometerInstance.WalkTenSteps()