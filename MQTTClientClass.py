from umqtt.simple import MQTTClient
import network
import utime

# Client to access the network and the Mosquitto Broker
# Allows publishing data to the broker

class MQTTClientClass:
	#Class stuff;
	client = None

	#Client Credentials:
	client_name = 'Intelliband'
	#client_ip = '192.168.0.10'
	client_ip = '192.168.43.182'
	#Server Credentials:

	## EERover
	# username = 'EEERover'
	# password = 'exhibition'

	## Mohamed's Phone
	username = 'Mohamed_Phone'
	password = 'EEEGroup'


	# Setting up the client class
	def __init__(self):

		## Setting up the network
		ap_if = network.WLAN(network.AP_IF)
		ap_if.active(False) #disable access point

		sta_if = network.WLAN(network.STA_IF)
		sta_if.active(True)

		sta_if.connect(self.username, self.password)

		self.client = MQTTClient(self.client_name, self.client_ip)

		## Checking to see if connected to the network
		while(not sta_if.isconnected()):
			print("Attempting to connect to server...")
   			utime.sleep_ms(500)

   		print("Connected to the server!")

   		##Connect to the broker if connected to the network
   		if (sta_if.isconnected()):
   			self.client.connect()


   	## Publish the data to the  broker with select topic and the package data
   	def publish_data(self, _topic, _data):
   		self.client.publish(_topic, _data);



