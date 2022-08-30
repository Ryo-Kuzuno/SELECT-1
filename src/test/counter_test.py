import sys
from tkinter import dialog
sys.path.append('../')
from counter import LS7366R
from time import sleep, time
import math
import RPi.GPIO as gpio


ls7366r = LS7366R(0, 4) #spi ce0 & byte mode=4
diameter=2      # [mm]
radius  = diameter/2
count   = 0
pos     = 0

while True: 
    try:
        count = ls7366r.read_counter()
        pos = 2 * math.pi * radius * count
        print("count: {}    position{}m\n".format(count, pos))

        sleep(1)

    except KeyboardInterrupt:
         print("Operation was killed!")
         ls7366r.close()
         gpio.cleanup()
         break
