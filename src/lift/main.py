import sys 
sys.path.append('../library')
from mission import Resilience


def main(): 
   distance = 80 # in meter  
   reduce_rate = 0.2   # Ratio of stop height to distance
   
   spec = {"radius": 0.03, "height": 2, "gear_ratio_enc2roller": 26/44} # in meter
   sensor = {"bme" : False, "sht" : False, "counter" : True}
   
   upper_limit = 10
   lower_limit = 1
   
   
   res = Resilience(upper_limit, lower_limit, spec, sensor)
   
   yesorno = input("Actuate motor? y/n\n")
   if yesorno =='y':
      res.run()
   elif yesorno =='n':
      print("Test aborting.")
   else:
      print("Unexpected word was input.")
   res.run()

if __name__ == "__main__": 
    main()
