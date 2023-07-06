import sys
sys.path.append('../library')
from time import sleep
from mission import Resilience

distance = 100 # in meter  
reduce_rate = 0.05
spec = {"radius": 0.3, "height": 2, "gear_ratio_enc2roller": 1/3} # in meter
sensor = {"bme" : False, "sht" : False, "counter" : True}

res = Resilience(distance, reduce_rate, spec, sensor)
print("Actuate signal waiting...")

while True: 
    try: 
        actuate_flag = res.twilite_remote.read_actuate()
        
        if actuate_flag==0:
            print("Ascending sequence starts in 10s.\n")
            for i in range(10):
                print(10-i)
                sleep(1)
            print("\nRun!\n")
            res.run()
            
    except KeyboardInterrupt: 
        print("Aborting the sequence.\n")
        res.twilite_remote.destroy()
        sys.exit()

