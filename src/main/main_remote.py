import main
import sys
from selemod import TWILITE_REMOTE

pin_remote_actuate=27
pin_remote_stop=26
twilite_remote=TWILITE_REMOTE(pin_remote_actuate,pin_remote_stop)

while True: 
    try: 
        actuate_flag = twilite_remote.read_actuate()
#       stop_flag = twilite_remote.read_stop()

        if actuate_flag==0:
            print("success")
            #main.main()

    except KeyboardInterrupt: 
        print("Aborting the sequence")
        twilite_remote.destroy()
        sys.exit()

