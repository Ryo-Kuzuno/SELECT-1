import sys
sys.path.append('../')
from time import sleep, time
import spidev 
from selemod import LS7366R
import math

encCounter = LS7366R(0, 1000000, 4)
diameter= 2e-3      # [mm]
radius  = diameter/2
count   = 0
pos     = 0
enc_val = 0

while True: 
    try:
        count = encCounter.read_counter()
        pos = 2 * math.pi * radius * count
        print("count: {}    position{}m\n".format(count, pos))
        

        sleep(0.001)

    except KeyboardInterrupt:
         print("Operation was killed!")
         encCounter.close()
         gpio.cleanup()
         break
