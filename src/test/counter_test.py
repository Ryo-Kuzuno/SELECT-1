import sys
from tkinter import dialog
sys.path.append('../')
from counter import LS7366R
from time import sleep, time
import math
import RPi.GPIO as gpio


ls7366r = LS7366R(0, 4) #spi ce0 & byte mode=4

while True: 
    try:
        ls7366r.count = ls7366r.ls7366r.read_counter()
        ls7366r.pos = 2 * math.pi * ls7366r.RADIUS * ls7366r.count
        print("count: {}    position{}m\n".format(ls7366r.count, ls7366r.pos))

        sleep(1)

    except KeyboardInterrupt:
         print("Operation was killed!")
         ls7366r.close()
         gpio.cleanup()
         break
