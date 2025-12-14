from utilities import *
import json
import paho.mqtt.client as mqtt
from datetime import datetime

debug_servos = False
game_state = False

servo_phi = Servo(0, duty_cycle_center=7.6, dc_min=5, dc_max=10, angle_range=45)
servo_theta = Servo(1, duty_cycle_center=7.6, dc_min=5, dc_max=10, angle_range=45)

laser = Laser(16)

# this callback runs once when the client connects with the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    #print('Subscribing to topic ', sub_topic_name)
    client.subscribe(controller_orientation_topic_name)
    client.subscribe(controller_trigger_topic_name)
    client.subscribe(controller_calibration_topic_name)
    client.subscribe(display_topic_name)

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    global game_state
    payload = msg.payload.decode("utf-8")
    topic = msg.topic

    if topic != controller_orientation_topic_name:
        now = datetime.now()
        print(now.strftime("%H:%M:%S: ") + payload)

    if topic == display_topic_name:
        if payload == "INITIALIZE_LASER":
            servo_phi.center()
            servo_theta.center()
            game_state = True
        
        if payload == "TURN_ON_LASER":
            laser.on()
        if payload == "TURN_OFF_LASER":
            laser.off()

        if payload == "END_GAME":
            laser.off()
            game_state = False
            
    elif topic == controller_orientation_topic_name:
        if game_state == True or debug_servos == True:
            payload_json = json.loads(payload)
            now = datetime.now()
            print(now.strftime("%H:%M:%S: Yaw: ") + str(payload_json["Yaw"]))
            print(now.strftime("%H:%M:%S: Pitch: ") + str(payload_json["Pitch"]))
            #print("Yaw: " + str(payload_json["Yaw"]))
            #print("Pitch: " + str(payload_json["Pitch"]))
            servo_phi.change_angle(payload_json["Yaw"])
            servo_theta.change_angle(payload_json["Pitch"])

    elif topic == controller_calibration_topic_name:
        #servo_phi.center()
        #servo_theta.center()
        #time.sleep(0.5)
        client.publish(pub_topic_name, payload="INITIALIZED", qos=0, retain=False)

# Read command line arguments and set the publish and subscribe topic names
# based on the command line arguments
my_name = "laser"
pub_topic_name = my_name
controller_orientation_topic_name = 'controller/orientation'
controller_trigger_topic_name = 'controller/trigger'
controller_calibration_topic_name = 'controller/calibration'
display_topic_name = "/display_team_laser_team"

# Initialize MQTT and connects to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.6.171", 1883, 60)
client.loop_start()

while 1:
    time.sleep(0.1)