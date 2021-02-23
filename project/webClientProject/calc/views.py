from django.shortcuts import render
from django.http import HttpResponse
from paho.mqtt import client as mqtt_client
import time


# Create your views here.
broker = '192.168.1.4'
port = 1883
#topic = "sakib/test"
client_id = '#test_ID_remote_admin_2'
username = 'sakib'
password = 'hd85512b'

def home(request):
    return render(request, 'home.html', {'name' : 'Sakib'})


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    
    return client


def publish(client, topic, msg):
    #msg_count = 0
     
    time.sleep(1)
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    #msg_count += 1



def add(request):
    client = connect_mqtt()
    client.loop_start()
    topic = request.POST['topic']
    msg = request.POST['msg']
    publish(client, topic = topic, msg = msg)
    client.disconnect()
    return render(request, 'result.html', {'result' : f"Sent `{msg}` to topic `{topic}`"})

    
