#!/usr/bin/env python3

from scan_stairs import scan
from stabilize_4 import stabilize
import time

stabilize(sec=3)

#scan()
#leg_pointが2つ以上の時に脚を動かし、１つしかないときは少しだけ前後に移動する