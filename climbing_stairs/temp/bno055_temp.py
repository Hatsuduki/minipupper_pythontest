#!/usr/bin/env python3

import adafruit_bno055
import board
import time

i2c = board.I2C()

sensor = adafruit_bno055.BNO055_I2C(i2c)

"""
print(sensor.axis_remap)
sensor.axis_remap = (0, 0, 0, 0, 0, 0)
print(sensor.axis_remap)
"""
while True:
    #print("acceleration: ", sensor.acceleration)
    #print("magnetic :", sensor.magnetic)
    print("gyro        : ", sensor.gyro)
    #print("euler       : ", sensor.euler) # yaw(z), roll(y), pitch(x)
    #print("quaternion  : ", sensor.quaternion)
    ##print("gravity     : ", sensor.gravity)
    #print(sensor.axis_remap)
    print()

    time.sleep(0.5)
