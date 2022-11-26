#!/usr/bin/bash

pip3 install --upgrade pip
#sudo apt install python-setuptools python3-setuptools

pip3 install sparkfun-qwiic-vl53l1x
#Doc https://qwiic-vl53l1x-py.readthedocs.io/en/latest/index.html#

pip3 install adafruit-circuitpython-bno055 
#Doc https://docs.circuitpython.org/projects/bno055/en/latest/#

pip3 install pigpio
sudo apt install python3-pigpio


#< sudo vi /lib/systemd/system/pigpiod.service >

#[Unit]
#Description=Daemon required to control GPIO pins via pigpio
#[Service]
#ExecStart=/usr/local/bin/pigpiod -l
#ExecStop=/bin/systemctl kill pigpiod
#Type=forking
#[Install]
#WantedBy=multi-user.target

sudo systemctl start pigpiod
sudo systemctl enable pigpiod
