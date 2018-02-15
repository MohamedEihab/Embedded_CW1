import paho.mqtt.client as mqtt
import time
import json
import matplotlib.pyplot as plt

#Empty initialised lists
stepsTaken = []
heartRate = []
timeTaken = []

#Plot graphs with hearbeat sensor, pedometer sensor data
#and time taken
def plot(a, b, xaxis, yaxis):
    plt.figure()
    plt.plot(a,b)
    plt.ylabel(yaxis)
    plt.xlabel(xaxis)

#Call back function tied to the client
#Extracts payload from MQTT JSON output
#Uses REGEX to extract numbers from heartrate and steps taken
def on_message(client, userdata, message):
    message_rec = str(message.payload.decode("utf-8"))

    first_limit = message_rec.find(': ')
    second_limit = message_rec.find(',')
    steps_taken = message_rec[first_limit+2:second_limit]

    third_limit = message_rec.find(': ', second_limit)
    fourth_limit = message_rec.find(',', second_limit+1)

    heart_rate = message_rec[third_limit + 2: fourth_limit-2]
   
    print("Steps Taken: %s"%steps_taken)

    print("Heart Rate: %s"%heart_rate) 

#Appends to lists in order to use in plotting function
    stepsTaken.append(int(steps_taken))
    heartRate.append(int(heart_rate))
    timeTaken.append(int(time.time() - startTime))

    #print("message topic=",message.topic)

#Store time at start of data being recieved    
startTimeEn = True
startTime = None

#Set up client 
client = mqtt.Client("ShreyBook")
#Link function to callback
client.on_message = on_message
#Input Broker IP
client.connect("192.168.43.167")

#Start client loop
client.loop_start()
if(startTimeEn):
    startTime = time.time()
    startTimeEn = False
client.subscribe("topic/state")
(client.on_message)

#End client loop after 30 seconds - configurable
#Plots graphs after this time
time.sleep(30) # wait
client.loop_stop()

#Graph plots only if length of a and b in plot(a,b) are the same
#Plot immediately if these two arrays have the same length
#Otherwise modify length of the longer array to match the shorter one 
if(len(heartRate)==len(stepsTaken) and len(heartRate)==len(timeTaken)):
    plot(stepsTaken,heartRate, 'Steps Taken', 'Heart rate /bpm')
    plot(timeTaken, stepsTaken, 'Time taken /s', 'Steps Taken')
    plot(timeTaken, heartRate, 'Time Taken /s', 'Heart Rate /bpm')
    plt.show()

