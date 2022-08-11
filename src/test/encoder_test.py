import sys
from tkinter import dialog
sys.path.append('../')
from selemod import Encoder
from time import sleep, time
import time
import RPi.GPIO as gpio
import math
import csv
import datetime

#このプログラムの起動は時限式にする
# もしくは、クライマーの高度が上端のダンパー付近に来た時に、起動する

gpio.setmode(gpio.BCM)

pin_A = 22
pin_B = 23
count = 0
precount = 0
sign = 0
lastB = 0
currentB = 0

goal=1
diameter=2
resolution=1

lim_rot = int(goal / (math.pi * diameter) * 1000)    # diameter[mm]
lim_pul = lim_rot * resolution

en_ = Encoder(pin_A, pin_B,  diameter, resolution, goal)

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(pin_A, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(pin_B, gpio.IN, pull_up_down=gpio.PUD_UP)
#gpio.setup(pin_signal, gpio.OUT, initial=gpio.LOW)

dt = datetime.datetime.now()
file_name = "encLog_" + str(dt.year) + "." + str(dt.month) + "." + str(dt.day + 4) + "_" + str(dt.hour + 20) + "." + str(dt.minute) + ".csv"
f = open(file_name, "a")
writer = csv.writer(f, lineterminator="\n")

        # datasize 2*20000
log = [[0.0, 0]]
for i in range(19999):
    log.append([0.0, 0])

sleep(0.5)
print(">> setup of encoder is done.")
print(">> lim_rot:%d, lim_pul = %d" % (lim_rot, lim_pul))


while True:
    try:
        encoder_deal=en_.deal()
        encoder_go=en_.go()

        sleep(1)

    except KeyboardInterrupt:
         print("Operation was killed!")
         en_.end()
         gpio.cleanup()
         break