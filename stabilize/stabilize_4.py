#!/usr/bin/python3

import pi_servo_hat
import time
import math
import adafruit_bno055
import board

I2C_ADDR = 0x40
pca9685 = pi_servo_hat.PiServoHat(address=I2C_ADDR)
pca9685.restart()

i2c = board.I2C()
bno = adafruit_bno055.BNO055_I2C(i2c)

def initPosition():
    #front-right
    pca9685.move_servo_position(15, 55) #top roll
    pca9685.move_servo_position(14, 35) #middle leg
    pca9685.move_servo_position(13, 35) #bottom leg
    
    #front-left
    pca9685.move_servo_position(12, 44) #top roll
    pca9685.move_servo_position(11, 72) #middle leg
    pca9685.move_servo_position(10, 65) #bottom leg

    #rear-right
    pca9685.move_servo_position(9, 50) #top roll
    pca9685.move_servo_position(8, 26) #middle leg
    pca9685.move_servo_position(7, 8) #bottom leg

    #rear-left
    pca9685.move_servo_position(6, 60) #top roll
    pca9685.move_servo_position(5, 86) #middle leg
    pca9685.move_servo_position(4, 90) #bottom leg

L1 = 50
L2 = 65
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
    pca9685.move_servo_position(7, the2*180/math.pi + 6)#6はL2のinitPositionから調整した角度

def servo_RL(x, z): #rear left
    ld = math.sqrt(x*x + z*z)
    phi = math.atan2(x, z)

    the1 = phi - math.acos((L1*L1 + ld*ld - L2*L2)/(2*L1*ld))
    the2 = math.acos((ld*ld - L1*L1 - L2*L2)/(2*L1*L2)) - 45*math.pi/180 + the1# -45はL1とL2のなす外側の角 - L1のz軸からの角度の大きさ

    pca9685.move_servo_position(5, -1*the1*180/math.pi + 35)#35はL1が垂直になる角度
    pca9685.move_servo_position(4, -1*the2*180/math.pi + 85)#85はL2のinitPosition角度

initPosition()

print("wait 3sec")
time.sleep(3)

FL_height = 83
FR_height = 83
RL_height = 83
RR_height = 83
between_sidelegs = 118
between_centerlegs = 86
deg_zero_offset_z = bno.euler[1]
deg_zero_offset_x = bno.euler[2]
Kp = 0.5
Kd = 1.1
while True: #PD制御 2 axes
    deg_z = bno.euler[1]
    deg_x = bno.euler[2]
    #print(deg_z)
    if deg_z != None and -17<deg_z and deg_z<17 and deg_x != None and -17<deg_x and deg_x<17:
        theta_z = (math.pi/180)*(deg_z - deg_zero_offset_z)
        theta_x = (math.pi/180)*(deg_x - deg_zero_offset_x)
        gyro_z = bno.gyro[1]
        gyro_x = bno.gyro[0]
        FL_height = FL_height - Kp*between_sidelegs/2*math.sin(theta_z) + Kd*gyro_z + Kp*between_centerlegs/2*math.sin(theta_x) - Kd*gyro_x
        FR_height = FR_height - Kp*between_sidelegs/2*math.sin(theta_z) + Kd*gyro_z - Kp*between_centerlegs/2*math.sin(theta_x) + Kd*gyro_x
        RL_height = RL_height + Kp*between_sidelegs/2*math.sin(theta_z) - Kd*gyro_z + Kp*between_centerlegs/2*math.sin(theta_x) - Kd*gyro_x
        RR_height = RR_height + Kp*between_sidelegs/2*math.sin(theta_z) - Kd*gyro_z - Kp*between_centerlegs/2*math.sin(theta_x) + Kd*gyro_x
        
        servo_FL(0, FL_height)
        servo_FR(0, FR_height)
        servo_RL(0, RL_height)
        servo_RR(0, RR_height)
        
    time.sleep(0.05)