import sys
sys.path.append('../../')
from selemod import E2S
from time import sleep, time
import time
import RPi.GPIO as gpio

#このプログラムの起動は時限式にする
# もしくは、クライマーの高度が上端のダンパー付近に来た時に、起動する

gpio.setmode(gpio.BCM)

pin_e2s_top = 16
pin_e2s_bottom = 20

e2s_ = E2S(pin_e2s_top, pin_e2s_bottom)

gpio.setup(pin_e2s_top,    gpio.OUT, initial=gpio.LOW)
gpio.setup(pin_e2s_bottom, gpio.OUT, initial=gpio.LOW)
gpio.setup(pin_e2s_top,    gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(pin_e2s_bottom, gpio.IN, pull_up_down=gpio.PUD_DOWN)

print("pin_e2s_top = %d\n" %pin_e2s_top)
print("pin_e2s_bottom = %d\n" %pin_e2s_bottom)

while True:
  try:
      top_sw_state    = e2s_.read_top()
      bottom_sw_state = e2s_.read_bottom()
      if top_sw_state == 1:
        print("top:",top_sw_state)
      if bottom_sw_state == 1:
        print("bottom",bottom_sw_state)

      sleep(1)
  except KeyboardInterrupt:
     print("Operation was killed!")
     e2s_.destroy()
     gpio.cleanup()
     break

