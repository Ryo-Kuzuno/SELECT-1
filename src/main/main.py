import sys 
sys.path.append('../')
from mission import Resilience
import selemod 
import RPi.GPIO as gpio 
import time 

def main(): 
    distance = 100 # in meter  
    reduce_rate = 0.05
    spec = {"radius": 0.3, "height": 2} # in meter
    sensor = {"bme" : False, "sht" : False, "counter" : True}
    res = Resilience(distance, reduce_rate, spec, sensor)
    
    #yesorno = input("Actuate motor? y/n\n")

    #if yesorno =='y':
    #   res.run()
    #elif yesorno =='n':
    #   print("Test aborting.")
    #else:
    #   print("Unexpected word was input.")
    res.run()

if __name__ == "__main__": 
    main()
