import time
import sys
import os
import spidev
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

PWM_PATH = "/sys/class/pwm/pwmchip0"

class HW_PWM:
    def __init__(self, frequency, channel):
        self.frequency = frequency 
        self.period = int(1000000000 / frequency)
        self.duty_cycle_percent = 0
        self.duty_cycle = 0
        self.channel = channel
        export_cmd = "echo " + str(channel) + " > " + PWM_PATH + "/export"
        enable_cmd = "echo 1 > " + PWM_PATH + "/pwm" + str(channel) + "/enable"
        print('Create PWM' + str(channel))
        print(export_cmd)
        os.system(export_cmd)
        time.sleep(0.5)

        print('Set the period')
        period = int(1000000000 / frequency)
        period_cmd = "echo " + str(period) + " > " + PWM_PATH + "/pwm" + str(channel) + "/period"
        print(period_cmd)
        os.system(period_cmd)
        time.sleep(0.5)

        print('Set duty cycle to 0')
        duty_cycle_cmd = "echo 0 > " + PWM_PATH + "/pwm" + str(channel) + "/duty_cycle"
        print(duty_cycle_cmd)
        os.system(duty_cycle_cmd)
        time.sleep(0.5)

        print('Enable PWM' + str(channel))
        print(enable_cmd)
        os.system(enable_cmd)
        time.sleep(0.5)

    def set_duty_cycle(self, duty_cycle_percent):
        # TODO: Complete this function
        if duty_cycle_percent > 100:
            duty_cycle_percent = 100
        if duty_cycle_percent < 0:
            duty_cycle_percent = 0
        
        duty_cycle_cmd = "echo " + str(int(duty_cycle_percent*self.period/100)) + " > " + PWM_PATH + "/pwm" + str(self.channel) + "/duty_cycle"
        os.system(duty_cycle_cmd)

class Servo(HW_PWM):
    def __init__(self, channel, duty_cycle_center=0.0, dc_min=0, dc_max=0, angle_range=0, frequency=50):
        self.duty_cycle_center = duty_cycle_center
        self.duty_cycle_min = dc_min
        self.duty_cycle_max = dc_max
        super().__init__(frequency, channel)

        self.angle_range = angle_range
        self.curr_angle = 0
        self.set_duty_cycle(duty_cycle_center)
        print("Initialization Complete")

    def center(self):
        self.set_duty_cycle(self.duty_cycle_center)

    def test_duty_cycle_inputs(self):
        while 1:
            user_dc = input("Enter duty cycle: ")
            self.set_duty_cycle(float(user_dc))

    def test_angle_inputs(self):
        while 1:
            user_angle = input("Enter angle: ")
            self.change_angle(float(user_angle))
    
    def test_ranges(self, incriment=0.1, sleep_time=0.1):
        curr_dc = self.duty_cycle_min
        incriment_direction = 1
        while 1:
            self.set_duty_cycle(curr_dc)
            curr_dc += incriment_direction * incriment
            if curr_dc > self.duty_cycle_max:
                curr_dc = self.duty_cycle_max
                incriment_direction = -1
            if curr_dc < self.duty_cycle_min:
                curr_dc = self.duty_cycle_min
                incriment_direction = 1
            time.sleep(sleep_time)
    
    def change_angle(self, angle):
        if angle > self.angle_range:
            angle = self.angle_range
        elif angle < -1 * self.angle_range:
            angle = -1 * self.angle_range
        
        new_duty_cycle = self.duty_cycle_center - (angle / (2*self.angle_range)) * (self.duty_cycle_max-self.duty_cycle_min)
        self.set_duty_cycle(new_duty_cycle)

class Laser():
    def __init__(self, pin):
        self.pin = pin
        self.state = 0
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = 1

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = 0

    def drive(self, state):
        GPIO.output(self.pin, state)
        self.state = state

    def toggle_state(self):
        self.state = not self.state
        GPIO.output(self.pin, self.state)