#!/usr/bin/env python3

import pigpio

pi = pigpio.pi()

print(pi.read(4))