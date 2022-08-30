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

pin_A = 22
pin_B = 23
diameter    =2      # [mm]
goal        =1
resolution  =1

en_ = Encoder(pin_A, pin_B,  diameter, resolution, goal)

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
