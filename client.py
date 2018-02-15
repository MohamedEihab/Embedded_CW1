import paho.mqtt.client as mqtt
import time
import json
import matplotlib.pyplot as plt

stepsTaken = []
heartRate = []
#JSONstring = 'None1'

def on_message(client, userdata, message):
    message_rec = str(message.payload.decode("utf-8"))
    print("message received " ,message_rec)
    #print(message_rec.find(': '))
    first_limit = message_rec.find(': ')
    second_limit = message_rec.find(',')
    steps_taken = message_rec[first_limit+2:second_limit]

    third_limit = message_rec.find(': ', second_limit)
    fourth_limit = message_rec.find(',', second_limit+1)

    heart_rate = message_rec[third_limit + 2: fourth_limit-2]

    print(steps_taken, heart_rate)
    stepsTaken.append(int(steps_taken))
    heartRate.append(int(heart_rate))


    print("message topic=",message.topic)
    return  "\'" + message_rec + "\'"


while(len(stepsTaken)<=10):
    client = mqtt.Client("ShreyBook")
    client.on_message = on_message
    client.connect("192.168.43.167")
    client.loop_start()
    client.subscribe("topic/state")
    print(client.on_message)
    '''parsed_json = json.loads(client.on_message)
    stepsTaken.append(parsed_json['Steps_Taken'])
    heartRate.append(parsed_json['Heart_Rate'])'''
    time.sleep(40) # wait
    client.loop_stop()

plt.plot(stepsTaken,heartRate)
plt.ylabel('Heart rate /bpm')
plt.xlabel('Steps taken')
plt.show()