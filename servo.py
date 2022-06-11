import pi_servo_hat
import time

I2C_ADDR = 0x40
pca9685 = pi_servo_hat.PiServoHat(address=I2C_ADDR)
pca9685.restart()

def setPosition():
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
    pca9685.move_servo_position(7, 17) #bottom leg

    #rear-left
    pca9685.move_servo_position(6, 55) #top roll
    pca9685.move_servo_position(5, 80) #middle leg
    pca9685.move_servo_position(4, 85) #bottom leg

#setPosition()

#if you want to make legs free
#pca9685.restart()

pca9685.move_servo_position(15, 50) #top roll
pca9685.move_servo_position(14, 60) #middle leg
pca9685.move_servo_position(13, 45) #bottom leg

#get current position
print(pca9685.get_servo_position(15))
print(pca9685.get_servo_position(14))
print(pca9685.get_servo_position(13))


