
import paho.mqtt.client as mqtt 
import time
import datetime
import Adafruit_DHT


now = datetime.datetime.now()

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

#mqtt Settings
broker_address="iot.eclipse.org"
topic1= "	jodib/temperature/sensor1"
topic2= "jodib/humidity/sensor1"

#DHT setting
sensor = Adafruit_DHT.DHT11
pin = 4

#threshold setting
maxTempThreshold = 27.0 #the optimum temp
minHumidThreshold = 70.0 #the lower the colder
maxHumidThreshold = 85.0 #the higher the hotter

print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

while True:
	try:
		humidity,temperature = Adafruit_DHT.read_retry(sensor,pin)
		if humidity is not None and temperature is not None:
			if temperature <= maxTempThreshold:
				client.loop_start() 
				client.publish(topic2,'{0:0.1f}'.format(temperature))
				print('Temp={0:0.1f}°C'.format(temperature))
				client.loop_stop() 
			else:
				#trigger relay	
				print('Temperature to hot');
			
			if humidity <= maxHumidThreshold:
				if humidity >= minHumidThreshold:
					client.loop_start() 
					client.publish(topic1,'{0:0.1f}'.format(humidity))
					print('Humidity={0:0.1f}%'.format(humidity))
					client.loop_stop()
				else:
					print('Humidity to cold');
			else:
				#trigger relay				
				print('Humidity to dry');
		else:
			client.loop_start() #start the loop
			client.publish(topic1,'N/A')
			print('Failed to get reading. try again')
			client.loop_stop() #stop the loop
	except RuntimeError as e:
			client.loop_start() #start the loop
			client.publish(topic1,'reading failed from DHT failure'.e.args)
			print('reading failed from DHT failure'.e.args)
			client.loop_stop() #stop the loop
			
	time.sleep(1)


