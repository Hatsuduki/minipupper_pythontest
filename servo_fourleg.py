#!/usr/bin/python3

import pi_servo_hat
import time
import math

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
    pca9685.move_servo_position(7, 17) #bottom leg

    #rear-left
    pca9685.move_servo_position(6, 55) #top roll
    pca9685.move_servo_position(5, 80) #middle leg
    pca9685.move_servo_position(4, 85) #bottom leg

L1 = 50
L2 = 56
def servo_FR(x, z): #front right
    ld = math.sqrt(x*x + z*z)
    phi = math.atan2(x, z)

    the1 = phi - math.acos((L1*L1 + ld*ld - L2*L2)/(2*L1*ld))
    the2 = math.acos((ld*ld - L1*L1 - L2*L2)/(2*L1*L2)) - 45*math.pi/180 + the1# -45はL1とL2のなす外側の角 - L1のz軸からの角度の大きさ

    pca9685.move_servo_position(14, the1*180/math.pi + 85)#85はL1が垂直になる角度
    pca9685.move_servo_position(13, the2*180/math.pi + 45)#45はL2のinitPosition角度
    #print(the1*180/math.pi + 85)
    #print(the2*180/math.pi + 45)

def servo_FL(x, z): #front left
    ld = math.sqrt(x*x + z*z)
    phi = math.atan2(x, z)

    the1 = phi - math.acos((L1*L1 + ld*ld - L2*L2)/(2*L1*ld))
    the2 = math.acos((ld*ld - L1*L1 - L2*L2)/(2*L1*L2)) - 45*math.pi/180 + the1# -45はL1とL2のなす外側の角 - L1のz軸からの角度の大きさ

    pca9685.move_servo_position(11, -1*the1*180/math.pi + 20)#20はL1が垂直になる角度
    pca9685.move_servo_position(10, -1*the2*180/math.pi + 60)#60はL2のinitPosition角度

def servo_RR(x, z): #rear right
    ld = math.sqrt(x*x + z*z)
    phi = math.atan2(x, z)

    the1 = phi - math.acos((L1*L1 + ld*ld - L2*L2)/(2*L1*ld))
    the2 = math.acos((ld*ld - L1*L1 - L2*L2)/(2*L1*L2)) - 45*math.pi/180 + the1# -45はL1とL2のなす外側の角 - L1のz軸からの角度の大きさ

    pca9685.move_servo_position(8, the1*180/math.pi + 70)#70はL1が垂直になる角度
    pca9685.move_servo_position(7, the2*180/math.pi + 17)#17はL2のinitPosition角度

def servo_RL(x, z): #rear left
    ld = math.sqrt(x*x + z*z)
    phi = math.atan2(x, z)

    the1 = phi - math.acos((L1*L1 + ld*ld - L2*L2)/(2*L1*ld))
    the2 = math.acos((ld*ld - L1*L1 - L2*L2)/(2*L1*L2)) - 45*math.pi/180 + the1# -45はL1とL2のなす外側の角 - L1のz軸からの角度の大きさ

    pca9685.move_servo_position(5, -1*the1*180/math.pi + 35)#35はL1が垂直になる角度
    pca9685.move_servo_position(4, -1*the2*180/math.pi + 85)#85はL2のinitPosition角度

initPosition()

time.sleep(1)

for j in range(-50, 51, 5): #test
    servo_FR(j, 75)
    servo_FL(j, 75)
    servo_RR(j, 75)
    servo_RL(j, 75)
    time.sleep(0.1)
for j in range(-50, 51, 5):
    servo_FR(-j, 75)
    servo_FL(-j, 75)
    servo_RR(-j, 75)
    servo_RL(-j, 75)
    time.sleep(0.1)
for j in range(-50, 51, 5):
    servo_FR(j, 75)
    servo_FL(j, 75)
    servo_RR(j, 75)
    servo_RL(j, 75)
    time.sleep(0.1)
