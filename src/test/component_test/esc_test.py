
# suppose test.py is at the same directory as selemod.py 

#import dependencies 
import sys 
sys.path.append('../')
import selemod
from time import sleep, time

# instantiate actuator class 
pin_esc = 18
pin_servo_1 = 23
# pin_servo_2 = 24
freq_esc = 50 
freq_servo = 50
brakeon_duty = 8.72 
brakeoff_duty = 4.85

pin_ec2_top = 16 
pin_ec2_bottom = 20

actu = selemod.Actuator(pin_esc=pin_esc, pin_servo_1=pin_servo_1, 
                        freq_esc=freq_esc, freq_servo=freq_servo, 
                        brakeon_duty=brakeon_duty, brakeoff_duty=brakeoff_duty)

# initial setup of esc
print("Have you calibrated the motor? (y/n)\n")
yesorno = input() 
if yesorno == 'n':
    print("Start caliberation.")
    actu.calibrate_esc()
    print("Actuate motor. y/n\n")
    yesorno = input()
    actu.brakeon()
    if yesorno == 'y':
        try:
            throttle = input("What throttle? Please type a value from 0 to 100.")
            throttle = float(throttle)
            print("throttle:", throttle)
            actu.new_throttle(throttle)
            sleep(10)
            actu.stop_esc(throttle)
            actu.brakeon()
            print("End test.")

        except KeyboardInterrupt:
            print("Operation aborted. Duty ratio start decreasing.")
            actu.stop_esc(throttle)
            print("Motor has stopped.")
    if yesorno == 'n':
        print("test aborted")

elif yesorno == 'y':
    actu.set_default_throttle()
    actu.brakeon()
    yesorno = input("Actuate motor. y/n")
    if yesorno == 'y':
        try:
            throttle = input("What throttle? Please type a value from 0 to 100.")
            throttle = float(throttle)
            print("throttle:", throttle)
            actu.new_throttle(throttle)
            sleep(10)
            actu.stop_esc(throttle)
            print("Brake working.")
            actu.brakeoff()
            print("End test.")

        except KeyboardInterrupt:
            print("Operation aborted. Duty ratio start decreasing.")
            actu.stop_esc(throttle)
            print("Motor has stopped.")
            actu.brakeoff()
            print("Brake working.")
    if yesorno == 'n':
        print("test aborted")


#throttle = [] #20 throttle points which correspond to 0~95 duty (5% increment -> 20data points)
#throttle_a0, throttle_a1 = actu.set_throttle(sampled_throttle)

# ec2 = test_ec2.EC2(pin_ec2_top, pin_ec2_bottom, actu)

# while True: 
#     actu.new_throttle(50)
#     ec2.read_top()
#     ec2.read_bottom()

# actu.end()
