import RPi.GPIO as GPIO
import time 

class E2S:
    def __init__(self, pin_e2s_top, pin_e2s_bottom): 
        """
        Argument
        ------------------------------------------
        pin_ec2top_ : ec2 corrector gpio
        pin_ec2_bottom : bottom ec2 corrector gpio 
        actu : actuator instance 
        """
        self.pin_e2s_top = pin_e2s_top
        self.pin_e2s_bottom = pin_e2s_bottom 
        GPIO.setup(pin_e2s_top, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pin_e2s_bottom, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def read_top(self): 
        top_sw_state = GPIO.input(self.pin_e2s_top)
        return top_sw_state 

    def read_bottom(self): 
        bottom_sw_state = GPIO.input(self.pin_e2s_bottom)
        return bottom_sw_state 

    def destoy(self): 
        GPIO.cleanup()