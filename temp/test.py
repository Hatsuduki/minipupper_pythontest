#!/usr/bin/env python3

import pigpio
import pi_servo_hat
import qwiic_vl53l1x
import adafruit_bno055
import board
import copy
import time
import numpy as np

def pigpio_test():
    pi = pigpio.pi()
    print(pi.read(4))

def pca9685_test(): #i2c address: 0x40
    pca = pi_servo_hat.PiServoHat(0x40)
    pca.restart()
    pca.move_servo_position(10, 60) #bottom leg
    #print(pca.get_pwm_frequency())
    print()

def vl53l1x_test(): #i2c address: 0x29
    tof = qwiic_vl53l1x.QwiicVL53L1X()
    print(tof.get_sensor_id())
    pca = pi_servo_hat.PiServoHat(0x40)
    pca.restart()

    pulse = [ i/10 for i in range(0, 460, 25)] #step 2.5°
    reverse = copy.deepcopy(pulse)
    reverse.reverse()
    pulse = pulse + reverse
    for i in pulse:
        pca.move_servo_position(2, i)
        time.sleep(0.3)

def bno055_test(): #i2c address: 0x28
    i2c = board.I2C()
    sensor = adafruit_bno055.BNO055_I2C(i2c)
    print(sensor.mode)

#pigpio_test()
#pca9685_test()
#vl53l1x_test()
#bno055_test()
