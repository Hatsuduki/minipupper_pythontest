#!/usr/bin/env python3

from scan_stairs import scan
import stabilize_4
import time


leg_point_x, leg_point_z = scan()

print(leg_point_x, leg_point_z)

stabilize_4.servo_FL(0, 40)
time.sleep(2)
stabilize_4.servo_FL(45+leg_point_x, 40)
time.sleep(2)
stabilize_4.servo_FL(45+leg_point_x, -1*leg_point_z-32)
time.sleep(1)
#stabilize(sec=3)

#scan()
#leg_pointが2つ以上の時に脚を動かし、１つしかないときは少しだけ前後に移動する