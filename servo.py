from utilities import *
import json
import paho.mqtt.client as mqtt

game_state = False

servo_phi = Servo(0, duty_cycle_center=7.6, dc_min=5, dc_max=10, angle_range=45)
servo_theta = Servo(1, duty_cycle_center=7.6, dc_min=5, dc_max=10, angle_range=45)

servo_phi.test_ranges()
servo_theta.test_ranges()

while 1:
    time.sleep(0.1)