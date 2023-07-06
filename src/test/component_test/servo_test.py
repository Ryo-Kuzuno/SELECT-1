import sys
sys.path.append('../')
import selemod
import time 
import RPi.GPIO as gpio 

pin_esc = 12
pin_servo_1 = 23
freq_esc = 50 
freq_servo = 50 
# servo duty min. = 4.85%, max. = 9.85%
brakeon_duty = 8.72 #4.85 + (9.85-4.85)*60/90
brakeoff_duty = 4.85

actu = selemod.Actuator(pin_esc=pin_esc, pin_servo_1=pin_servo_1, freq_esc=freq_esc, freq_servo=freq_servo, brakeon_duty=brakeon_duty, brakeoff_duty=brakeoff_duty)

while True: 
    try: 
        print('[brake status]: OFF\n')
        actu.brakeoff()
        time.sleep(1)

        print('[brake status]: ON\n')
        actu.brakeon()
        time.sleep(1)

    except KeyboardInterrupt: 
        actu.ser_1.stop()
        actu.ser_2.stop()
        gpio.cleanup()
        sys.exit()