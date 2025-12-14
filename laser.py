from utilities import *

GPIO.setmode(GPIO.BOARD)

laser = Laser(16)

while 1:
    print("Laser state: " + str(laser.state))
    laser.toggle_state()
    user_input = input("Press enter to switch the laser on and off")