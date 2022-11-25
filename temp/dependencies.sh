#!/usr/bin/bash


pip3 install --upgrade pip
#sudo apt install python-setuptools python3-setuptools

pip3 install sparkfun-qwiic-vl53l1x
#Doc https://qwiic-vl53l1x-py.readthedocs.io/en/latest/index.html#

pip3 install adafruit-circuitpython-bno055 
#Doc https://docs.circuitpython.org/projects/bno055/en/latest/#

pip3 install pigpio
sudo apt install python-pigpio python3-pigpio
sudo systemctl start pigpiod
sudo systemctl enable pigpiod
