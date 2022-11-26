#!/usr/bin/env python3

import pigpio
import pi_servo_hat
import qwiic_vl53l1x
import adafruit_bno055
import board

def pigpio_test():
    pi = pigpio.pi()
    print(pi.read(4))

def pca9685_test(): #i2c address: 0x40
    pca = pi_servo_hat.PiServoHat(0x40)
    pca.restart()
    print(pca.get_pwm_frequency())
    print()

def vl53l1x_test(): #i2c address: 0x29
    tof = qwiic_vl53l1x.QwiicVL53L1X()
    print(tof.get_sensor_id())

def bno055_test(): #i2c address: 0x28
    i2c = board.I2C()
    sensor = adafruit_bno055.BNO055_I2C(i2c)
    print(sensor.mode)

#pigpio_test()
#pca9685_test()