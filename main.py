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

# I2Cport to connect to the accelerometer
i2cport_acc = I2C(scl = Pin(2), sda = Pin(16), freq = 100000)

# I2Cport to connect to Luxsensor
i2cport =I2C(scl=Pin(5), sda=Pin(4), freq=100000)

# Turning on the Lux Sensor
i2cport.writeto_mem(SLAVE_ADDRESS, 0, b'\0x03')

#Accelerometer setup
i2cport_acc.writeto_mem(24, 0x1F, b'\0xC0')
i2cport_acc.writeto_mem(24, 0x23, b'\0x80')
i2cport_acc.writeto_mem(24, 0x20, bytearray([0x4F]))

#LED Pin
LED_out = machine.Pin(15, machine.Pin.OUT)

# Tuples for sensor data
lux_sensor = {'channel_0': 0, 'channel_1' : 0} # Packaged Sensor Data
temp_sensor = {'temperature' : 0} # Packaged Temperature Data
gyro = {'x_dir' : 0, 'y_dir' : 0, 'z_dir' : 0} # Packaged Gyro

broker_package = {'Steps_Taken' : 0, 'Heart_Rate' : 0} # Server message package

# Signs the input x
def to_signed(x):
    xor_bits = 0xFFFF
    if x>=0x7FFF:
        y = x ^ xor_bits
        y=0-(y+1)
    else: 
        y=x
    return y

# Takes the raw data from the sensors
# Mutates them into a suitable form, changing the data into measurable units
# Inputs the data into the packages
def process_input_data():

    #lux input sensor data
    data0low = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8C,1),'big')
    data0high = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8D,1),'big')

    data1low = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8E,1),'big')
    data1lhigh = int.from_bytes(i2cport.readfrom_mem(SLAVE_ADDRESS,0x8F,1),'big')

    # Two data channel from the lux combining the high and low data
    channel0 = data0high*256 + data0low
    channel1 = data1lhigh*256 + data1low

    # Inputting the data into the package
    lux_sensor['channel_0'] = channel0
    lux_sensor['channel_1'] = channel1

    #temperature data
  #  temp_low = int.from_bytes(i2cport_acc.readfrom_mem(24,0x0C,1),'big')
  #  temp_high = int.from_bytes(i2cport_acc.readfrom_mem(24,0x0D,1),'big')

  #  temp_sensor['temperature'] = 256*temp_high + temp_low

    # Accelerometer data : read X Y Z from relevant registers in memory
    X_L = i2cport_acc.readfrom_mem(24, 0x28, 1)
    X_H = i2cport_acc.readfrom_mem(24, 0x29, 1)
    Y_L = i2cport_acc.readfrom_mem(24, 0x2A, 1)
    Y_H = i2cport_acc.readfrom_mem(24,0x2B, 1)
    Z_L = i2cport_acc.readfrom_mem(24, 0x2C, 1)
    Z_H = i2cport_acc.readfrom_mem(24,0x2D,1)

    # Converts data into integer and shifts : low power mode is 8 bits 
    #left aligned
    x_comb = int.from_bytes(X_H,'big')<<8
    y_comb = int.from_bytes(Y_H,'big')<<8
    z_comb = int.from_bytes(Z_H,'big')<<8
    
    # Converts from unsigned to signed int
    x_combf = float(to_signed(x_comb))
    y_combf = float(to_signed(y_comb))
    z_combf = float(to_signed(z_comb))

    # Convert to m/s^2 by dividing by 2g
    x_combf = x_combf*10/TWOG 
    y_combf = y_combf*10/TWOG
    z_combf = z_combf*10/TWOG

    # Inputs the data into the accelerometer package
    gyro['x_dir'] = x_combf
    gyro['y_dir'] = y_combf
    gyro['z_dir'] = z_combf

    return

counter = 0 # Keeps track of the time
time = 0 # Total elapsed time
delay = 20 #delay in ms
simulated_bpm = 70 # The simulated BPM for the LED
duty_time = (60/simulated_bpm)/2 # How long the LED should be on and off for the simulated BPM
duty_counter = duty_time / (delay/1000) # How many delays should we wait before flipping the LED
led_switch = 0 # Turns on the LED 

# Instances of the classes used 
HeartRateClass = HeartRateProcessor.HeartRateProcessorClass(delay)
PedometerInstance= PedometerClass.PedometerClass()
MQTTClientInstance = MQTTClientClass.MQTTClientClass()

# The main loop for running the device
while(True):

    process_input_data() # Take in the raw data from the sensors

    HeartRateClass.process_raw_lux(lux_sensor['channel_1']) # Process the data in the heart rate class
    PedometerInstance.process_raw_data(gyro['x_dir'], gyro['y_dir'], gyro['z_dir']) # Process the data in the pedometer class

    broker_package['Steps_Taken'] = PedometerInstance.getSteps() # Package the steps taken
    broker_package['Heart_Rate'] = HeartRateClass.getHeartRate() # Package the result heartrate
    MQTTClientInstance.publish_data('topic/state', bytes(ujson.dumps(broker_package), 'utf-8')); # Publish the data to the server

    # Duty counter for the LED
    if (counter < duty_counter):
        counter += 1

    else:
        counter = 0
        if (led_switch == 0):
            led_switch = 1
            LED_out.on() # Switches the LED on
        else:
            led_switch = 0
            LED_out.off() # Switches the LED off


    utime.sleep_ms(delay) # 20 readings in a second
    time += delay # Elapsed time

    if (time % 1000 == 0):
        print("Steps Taken:", PedometerInstance.getSteps()) ## Every second print the steps taken
        
        if (time % 5000 == 0):
            print("Elapsed Time: ", time/1000) # Every 5 seconds print the elapsed time

