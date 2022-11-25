#!/usr/bin/python3

import pi_servo_hat
import time

I2C_ADDR = 0x40
pca9685 = pi_servo_hat.PiServoHat(address=I2C_ADDR)
pca9685.restart()

def initPosition():
    #front-right
    pca9685.move_servo_position(15, 50) #top roll
    pca9685.move_servo_position(14, 45) #middle leg
    pca9685.move_servo_position(13, 45) #bottom leg
    
    #front-left
    pca9685.move_servo_position(12, 50) #top roll
    pca9685.move_servo_position(11, 60) #middle leg
    pca9685.move_servo_position(10, 60) #bottom leg

    #rear-right
    pca9685.move_servo_position(9, 55) #top roll
    pca9685.move_servo_position(8, 37) #middle leg
    pca9685.move_servo_position(7, 13) #bottom leg

    #rear-left
    pca9685.move_servo_position(6, 55) #top roll
    pca9685.move_servo_position(5, 80) #middle leg
    pca9685.move_servo_position(4, 85) #bottom leg

initPosition()
time.sleep(0.1)

pca9685.restart()

print("release servo")
