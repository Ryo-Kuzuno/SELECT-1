import sys
sys.path.append('../library/')
from selemod import Actuator
import sys 

pin_esc = 18
pin_servo_1 = 23
# pin_servo_2 = 24
freq_esc = 50 
freq_servo = 50
brakeon_duty = 8.72 
brakeoff_duty = 4.85

pin_ec2_top = 16 
pin_ec2_bottom = 20

actu = Actuator(pin_esc=pin_esc, pin_servo_1=pin_servo_1, 
                freq_esc=freq_esc, freq_servo=freq_servo, 
                brakeon_duty=brakeon_duty, brakeoff_duty=brakeoff_duty)


while True: 
    try: 
        print('Want to calibrate esc? (y/n)')
        inp = input()
        if inp == "y":
            actu.calibrate_esc()
            break
        elif inp == "n": 
            actu.set_default_throttle()
            input("Press Enter to move another operation...")
            break
        else:
            print('Please input y or n.')
            
    except KeyboardInterrupt: 
        print("Aborting the sequence")
        sys.exit()


