import sys
sys.path.append('../')
from selemod import Actuator
import sys 
from mission import Resilience

while True: 
    try: 
        print('Want to calibrate esc? (y/n)')
        inp = input()
        if inp == "y":
            Actuator.calibrate_esc()
            break
        elif inp == "n": 
            Actuator.set_min_throttle()
            break
        else:
            print('Please input y or n.')
            
    except KeyboardInterrupt: 
        print("Aborting the sequence")
        sys.exit()


