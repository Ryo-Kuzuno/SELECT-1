from selemod import Actuator, E2S

pin_esc = 18
pin_servo_1 = 23
pin_servo_2 = 24
freq_esc = 50 
freq_servo = 50
brakeon_duty = 8.72 
brakeoff_duty = 4.85

pin_ec2_top = 16 
pin_ec2_bottom = 20

actu = selemod.Actuator(pin_esc=pin_esc, pin_servo_1=pin_servo_1, 
                        pin_servo_2=pin_servo_2, freq_esc=freq_esc, 
                        freq_servo=freq_servo, brakeon_duty=brakeon_duty, 
                        brakeoff_duty=brakeoff_duty)

#initial setup of esc
actu.test_esc()
throttle = [] #20 throttle points which correspond to 0~95 duty (5% increment -> 20data points)

ec2 = test_ec2.EC2(pin_ec2_top, pin_ec2_bottom, actu)

while True: 
    actu.new_throttle(50)
    ec2.read_top()
    ec2.read_bottom()

actu.end()