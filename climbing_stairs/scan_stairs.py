#!/usr/bin/env python3

import pigpio
import time
import copy
import sys
import signal
import qwiic_vl53l1x
import statistics
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import pi_servo_hat


pulse = [ i/10 for i in range(0, 460, 25)] #step 2.5°
theta = [(i/10)*np.pi/180 for i in range(0, 450+1, 25)]  # 0°~45° by 2.5°

def scan():
    pi = pigpio.pi()

    pca9685 = pi_servo_hat.PiServoHat(0x40)
    pca9685.restart()

    # ToF setting
    ToF = qwiic_vl53l1x.QwiicVL53L1X()

    if (ToF.sensor_init() == None):		 # Begin returns 0 on a good init
        print("Sensor online!\n")

    ToF.set_distance_mode(1)	
    ToF.set_inter_measurement_in_ms(60)
    ToF.set_timing_budget_in_ms(30)
    ToF.set_roi(12, 6, 59)

    running = True
    """
    def exit_handler(signal, frame):
        global running
        running = False
        time.sleep(0.5)
        ToF.stop_ranging()
        pca9685.move_servo_position(2, pulse[0])
        print()
        sys.exit(0)
    """
    def exit_handler():
        global running
        running = False
        time.sleep(0.5)
        ToF.stop_ranging()
        pca9685.move_servo_position(2, pulse[0])
        print()
        #sys.exit(0)

    # Attach a signal handler to catch SIGINT (Ctrl+C) and exit gracefully
    signal.signal(signal.SIGINT, exit_handler)


    count = 0
    distance = [] # Initialize list
    three_point = []
    line_x = []
    line_z = []
    avg_slope = 0
    pre_slope = 0
    line_flag = True
    total_x = []
    total_z = []
    first_flag = True
    first_axis = []
    rotate_deg = 21

    # Graph setting
    fig, ax = plt.subplots()
    ax.plot(0, 0,  marker="o", color="red", linestyle="None")

    ToF.start_ranging()		
    time.sleep(0.15)

    #while running:
    for k in theta:
        #start = time.time()
        #pi.set_servo_pulsewidth(21, pulse[count])   #set servo
        pca9685.move_servo_position(2, pulse[count])

        try:
            for i in range(10):
                time.sleep(0.06)
                distance.append(ToF.get_distance()+20)  # Get the result of the measurement from the sensor
            
        except Exception as e:
            print(e)

        print(distance)
        avgdistance = statistics.mean(distance) # Running average of last 10 measurements
        distance.clear()
        
        if first_flag == True:
            x = avgdistance*np.sin(theta[count])
            z = -1*avgdistance*np.cos(theta[count])
            first_axis.append(x)
            first_axis.append(z)
            first_flag = False
        else:
            x = (avgdistance*np.sin(theta[count]) - first_axis[0])*np.cos(rotate_deg*np.pi/180) - (-1*avgdistance*np.cos(theta[count]) - first_axis[1])*np.sin(rotate_deg*np.pi/180) + first_axis[0]
            z = (avgdistance*np.sin(theta[count]) - first_axis[0])*np.sin(rotate_deg*np.pi/180) + (-1*avgdistance*np.cos(theta[count]) - first_axis[1])*np.cos(rotate_deg*np.pi/180) + first_axis[1]
        #print(x, z)
        total_x.append(x)
        total_z.append(z)
    
        #end = time.time()
        #print("avgDistance(mm): %.2f     deg: %.2f    count: %s    time: %.2f" % (avgdistance, theta[count]*180/np.pi, count, (end-start)))#AAA
    
        if 10 < avgdistance and avgdistance < 200:  # distance threshold
            if line_flag == True:
                line_x.append(x)# start point
                line_z.append(z)
                line_flag = False
            three_point.append([x, z])
            if len(three_point) > 3:
                del three_point[0]

        if len(three_point) >= 3:
            slope_1 = (three_point[1][1] - three_point[0][1]) / (three_point[1][0] - three_point[0][0]) # average slope of two former
            slope_2 = (three_point[2][1] - three_point[1][1]) / (three_point[2][0] - three_point[1][0]) # of two latter
            avg_slope = (slope_1 + slope_2) / 2 # of all
        
        if (avg_slope > pre_slope and avg_slope > 1) or (count == len(theta)-1):# 傾きが前のやつより大きくて1以上　または　前のやつより小さくて１以下   
            if three_point[0][0] - line_x[len(line_x)-1] > 10:
                pre_z = line_z[len(line_z)-1]
                line_x.append(three_point[0][0])
                line_z.append(pre_z)
        if avg_slope < pre_slope and avg_slope < 1:
            if three_point[0][1] - line_z[len(line_z)-1] > 10:
                pre_x = line_x[len(line_x)-1]
                line_x.append(pre_x)
                line_z.append(three_point[0][1])

        pre_slope = avg_slope

        count += 1

        if count >= len(theta):
            line_flag = True
            first_flag = True
            leg_point_x = []
            leg_point_z = []
            for i in range(len(line_x)):
                if i%2 == 1:
                    leg_point_x.append((line_x[i]+line_x[i-1])/2)
                    leg_point_z.append(line_z[i])

            plt.cla()
            ax.set_aspect("equal")
            ax.set_xlabel("x")
            ax.set_ylabel("z")
            ax.grid(ls=":")
            ax.set_xlim([-40, 120])
            ax.set_ylim([-160, 9])
            ax.plot(line_x, line_z, marker=".", color="black")
            #ax.plot(total_x, total_z, marker=".", color="red", linestyle="None")
            ax.plot(leg_point_x, leg_point_z, marker=".", color="red", linestyle="None")

            pca9685.move_servo_position(2, pulse[0])
            time.sleep(1)

            distance.clear()
            three_point.clear()
            line_x.clear()
            line_z.clear()
            total_x.clear()
            total_z.clear()
            avg_slope = 0
            pre_slope = 0
            print()
            plt.savefig('./img/figure_00.png')

            count = 0

    exit_handler()
        