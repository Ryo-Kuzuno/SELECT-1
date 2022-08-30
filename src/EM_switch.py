import RPi.GPIO as GPIO
import time 

class EM_SW:
    def __init__(self, pin_em_sw): 
        """
        Argument
        ------------------------------------------
        pin_em_sw : emergency switch signal gpio 
        """
        self.pin_em_sw = pin_em_sw
        GPIO.setup(self.pin_em_sw, GPIO.IN, GPIO.PUD_UP) #switch is connected with pull-up  
    
    def read(self): 
        """switch not pressed => 1  switch pressed => 0"""
        em_sw_state = GPIO.input(self.pin_em_sw)
        return em_sw_state   

    def destoy(self): 
        GPIO.cleanup()
        sys.exit()