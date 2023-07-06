
# suppose test.py is at the same directory as selemod.py 

#import dependencies 
import sys 
sys.path.append('../library/')
from selemod import Actuator

# instantiate actuator class 
pin_esc = 18
pin_servo_1 = 23
# pin_servo_2 = 24
freq_esc = 50 
freq_servo = 50
brakeon_duty = 8.72 
brakeoff_duty = 4.85
throttle_a0 = 5.15
throttle_a1 = 0.047

pin_ec2_top = 16 
pin_ec2_bottom = 20

actu = Actuator(pin_esc=pin_esc, pin_servo_1=pin_servo_1, 
                        freq_esc=freq_esc, freq_servo=freq_servo, 
                        brakeon_duty=brakeon_duty, brakeoff_duty=brakeoff_duty,
                        throttle_a0=throttle_a0, throttle_a1=throttle_a1)

actu.check_brake()
