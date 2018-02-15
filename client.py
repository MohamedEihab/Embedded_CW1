import paho.mqtt.client as mqtt
import time
import json
import matplotlib.pyplot as plt

x = [None]*1000
y = [None]*1000
z = [None]*1000

def on_message(client, userdata, message):
    message_rec = str(message.payload.decode("utf-8"))
    print("message received " ,message_rec)
    print("message topic=",message.topic)
    return message_rec

client = mqtt.Client("ShreyBook")

client.on_message = on_message

client.connect("192.168.43.167")
while(len(x)<=1):
    client.loop_start()
    client.subscribe("topic/state")
    parsed_json = json.loads(client.on_message)
    z.append(parsed_json['z_dir'])
    y.append(parsed_json['y_dir'])
    x.append( parsed_json['x_dir'])
    time.sleep(4000) # wait
    client.loop_stop()

plt.plot(x,y)
plt.ylabel('Acceleration m/s^2')
plt.show()