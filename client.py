import paho.mqtt.client as mqtt
import time
import json
import matplotlib.pyplot as plt

stepsTaken = []
heartRate = []
timeTaken = []

def plot(a, b, xaxis, yaxis):
    plt.plot(a,b)
    plt.ylabel(yaxis)
    plt.xlabel(xaxis)
    plt.show()

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

    stepsTaken.append(int(steps_taken))
    heartRate.append(int(heart_rate))

    #print("message topic=",message.topic)
    #return  "\'" + message_rec + "\'"
startTimeEn = True
startTime = None

client = mqtt.Client("ShreyBook")
client.on_message = on_message
client.connect("192.168.43.167")

client.loop_start()
if(startTimeEn):
    startTime = time.time()
    startTimeEn = False
client.subscribe("topic/state")
(client.on_message)
timeTaken.append(time.time() - startTime)

time.sleep(10) # wait
client.loop_stop()

plot(stepsTaken,heartRate, 'Steps Taken', 'Heart rate /bpm')
plot(timeTaken, stepsTaken, 'Time taken /s', 'Steps Taken')
