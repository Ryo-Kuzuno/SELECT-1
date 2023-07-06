import RPi.GPIO as gpio
from smbus import SMBus
from time import sleep, time
import csv
import math
import datetime
import sys
import spidev 


class Actuator:

    def __init__(self, pin_esc:int, pin_servo_1:int, freq_esc:int, freq_servo:int,
                brakeon_duty:float, brakeoff_duty:float):

        """
        pin_esc: pin number in BCM(The number of xx of GPIOxx) connected with a ESC's signal line
        pin_servo_1: pin number in BCM connected with a signal line of a servo
        freq_esc[Hz]: frequency of signals to ESC
        freq_servo[Hz]: frequency of signals to servo
        brakeon_duty: duty to brake on
        brakeoff_duty: duty to brake off
        throttle_a0: a constant of a duty-throttle relation
        throttle_a1: a coefficient of a duty-throttle relation
        constup_throttle: throttle value to go up at a contsant speed
        --------------------------------------------
        
        """

        # setup properties
        self.esc_type = 'bidir'
        self.pin_esc = pin_esc
        self.freq_esc = freq_esc
        self.freq_servo  = freq_servo
        self.pin_servo_1 = pin_servo_1
        self.brakeon_duty = brakeon_duty
        self.brakeoff_duty = brakeoff_duty
        self.decrease_rate = 0.1

        if self.esc_type == 'onedir':
            self.max_pulsewidth = 1970
            self.min_pulsewidth = 1030
            self.mid_pulsewidth = 1500
            print("One-directional esc")

            pulseperiod = 1/self.freq_esc
            self.max_duty = self.max_pulsewidth / 10**6 / pulseperiod * 100
            self.min_duty = self.min_pulsewidth / 10**6 / pulseperiod * 100
            self.mid_duty = self.mid_pulsewidth / 10**6 / pulseperiod * 100

            self.throttle_a0 = 5.15     # duty vs throttle bias
            self.throttle_a1 = 0.047    # duty vs throttle weight (this was estiamted from linear regression)
            self.default_duty   = self.min_duty


        elif self.esc_type == 'bidir':
            self.max_pulsewidth = 2000
            self.min_pulsewidth = 1000
            self.mid_pulsewidth = 1500
            print("Bi-directional esc")

            pulseperiod = 1/self.freq_esc
            self.max_duty = self.max_pulsewidth / 10**6 / pulseperiod * 100
            self.min_duty = self.min_pulsewidth / 10**6 / pulseperiod * 100
            self.mid_duty = self.mid_pulsewidth / 10**6 / pulseperiod * 100

            self.throttle_a0 = self.mid_duty    # duty throttle offset
            self.throttle_a1 = 0.015            # duty vs throttle weight (this was estiamted from linear regression)
            self.default_duty   = self.mid_duty
        else:
            print("incorrect key of esc_type")
            sys.exit()


        """
        self.tune_const_speed = None
        self.tune_initial_duty = None
        self.tune_const_duty = None
        """

        # internal setup
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)      
        gpio.setup(self.pin_esc, gpio.OUT)
        gpio.setup(self.pin_servo_1, gpio.OUT)    
        self.esc = gpio.PWM(self.pin_esc, freq_esc)
        self.ser_1 = gpio.PWM(self.pin_servo_1, freq_servo)
        self.esc.start(0)
        self.ser_1.start(self.brakeon_duty)
    
    def calibrate_esc(self):
        """
        ESC needs calibration when connecting transmitter to ESC for the first time.
        """ 

        print("initializing esc, remove battery...")
        

        self.esc.ChangeDutyCycle(self.max_duty)
        print("\nsetting esc max pulse\n")
        print("Maximum duty ratio: %.1f\n" %self.max_duty)

        print("connect battery. Press Enter after the beep.")
        inp = input()
        if inp == '':
            self.esc.ChangeDutyCycle(self.default_duty)
            print("Default duty ratio: %.1f\n" %self.default_duty)

            print("Is the motor silent? y/n")
            yesorno = input()
            if yesorno == 'y':
                print("Calibration has completed.")
                sleep(1)


    def set_default_throttle(self):
        """
        This function is used before you start rotating motor. 
        Setting minimum throttle is needed before sending specified PWM pulse.
        You need to confirm whether the set minimum throttle is valid by executing calibrate_esc().
        """

        duty_initial = self.default_duty
        print("duty:", duty_initial)
        self.esc.start(duty_initial)
        sleep(2)
        print("Motor is ready.\n")


    def test_esc(self):
        """
        drive a motor as a test, changing its duty from 0% to 95% every 5 secs,
        and from 95% to 0% every 0.5 secs.

        this method is for confirming the duty-throttle relation.
        so you had better make a record of the throttle data corresponded to the duty.
        you can use the throttle data and culculate the duty-throttle relation as linear-relation model.
        """
         #starting to rotate at duty ratio 7.5 because intermediate point pulse width is 1.5msec
        duty_step = 0.5
        upper_limit = 0.9*self.max_duty
        duty_count = round((upper_limit-duty_initial)/duty_step)
        self.set_default_throttle()



        print("Is the motor silent? y/n")
        yesorno = input()
        if yesorno == 'y':
            print("Setting has completed. Start? y/n")
            yesorno = input()

            if yesorno == 'y': 
                try:
                    #for i in range(0, duty_count):
                    #    duty = i * duty_step  + duty_initial
                    #    print("duty:", duty)
                    #    self.esc.ChangeDutyCycle(duty)
                    #    sleep(1)
                    #
                    duty = 7.1
                    print("duty:", duty)
                    self.esc.ChangeDutyCycle(duty)
                    sleep(15)
                    self.stop_esc(duty)
                    print("This test has ended.")

                except KeyboardInterrupt:
                    print("Operation aborted.")
                    self.stop_esc(duty)
                    

            else :
               print("end")
               return

        else :
            print("Configuration error.")
            return

    def stop_esc(self,throttle):
        """
        ESC should be slow gradualy.
        """ 
        print("Duty ratio decreasing.")
        # duty = self.throttle_a0 + self.throttle_a1*throttle
        duty = self.throttle_a0 + self.throttle_a1 * throttle
        delta = self.decrease_rate*(duty-self.default_duty)
        for i in range(round(1/self.decrease_rate)):
            duty = duty-delta
            #print("Duty:", duty)
            self.esc.ChangeDutyCycle(duty)
            sleep(.01)
        print("Motor stop")


    @staticmethod
    def LSM(x, y)-> "return a tuple of the coefficients (a0, a1)":
        """
        x: list or tuple of data of parameter for estimation
        y: list or tuple of data to be estimated
        """
        num = float(len(x))
        sum_x = float(sum(x))
        sum_y = float(sum(y))
        sum_x2 = float(sum([i ** 2.0 for i in x]))
        sum_xy = float(sum([i * j for i, j in dict(x, y)]))
        denominator = sum_x**2.0 - num * sum_x2

        a0 = (sum_x * sum_xy - sum_x2 * sum_y) / denominator
        a1 = (sum_x * sum_y - num * sum_xy) / denominator

        return a0, a1

    def set_throttle(self, throttles:(list, tuple), show = False)->"return a tuple of two coeffients of a duty-throttle relation":
        """
        throttles: a list or tuple with data of throttle value which is corresponded to the list of duty 0~95, whose length is 20.
        show: True -> print the result of culculation
                   -> not print it
        """
        type_throttles = type(throttles)
        if type_throttles != type(list()) and type_throttles != type(tuple()):
            print("the argument type is not available; make it as a list or tuple")
            self.end()
            sys.exit()

        if len(throttles) != 20:
            print("the length of argument is not 20.")
            self.end()
            sys.exit()

        throttle_worth = []
        index_worth = []
        for i, value in enumerate(throttles):
            if value > 0 or value < 100:
                throttle_worth.append(value)
                index_worth.append(i)
            else:
                pass

        duties = [i * 5.0 for i in index_worth]
        self.throttle_a0, self.throttle_a1 = Actuator.LSM(throttle_worth, duties)

        if show == True:
            print("a0:", round(self.throttle_a0), 2)
            print("a1:", round(self.throttle_a1), 2)
            return self.throttle_a0, self.throttle_a1
        elif show == False:
            return self.throttle_a0, self.throttle_a1

    # esc
    def new_throttle(self, throttle:float):
        """
        throttle: throttle value you want to change to
        -------------------------------------------------
        this method changes current duty to new duty calcurated with the throttle argument you give.
        [note] 0 <= throttle <= 100.
        """
       
        if self.throttle_a0 == None:
            print("throttle_a0 doesn't have a value. execute test_esc() and set_throttle(), and set the value of throttle_a0.")
            self.end()
            sys.exit()
        elif self.throttle_a1 == None:
            print("throttle_a1 doesn't have a value. execute test_esc() and set_throttle(), and set the value of throttle_a0.")
            self.end()
            sys.exit()
        
        duty =  self.throttle_a0 + self.throttle_a1 * throttle
        #duty = round(duty,1)
        duty_step = 0.5
        duty_count = round(duty/duty_step)
        
        print("duty:", duty)
        # while motion flag is True, keep motor on 
        self.esc.ChangeDutyCycle(duty)
        sleep(0.1)
        # self.stop_esc(duty)

    def new_duty(self, duty:float):
        """
        duty: duty value you want to change to
        ---------------------------------------
        this method changes current duty to new duty you specify
        """

        if duty < 0:
            duty = 0
        elif duty > 100:
            duty = 100

        self.esc.ChangeDutyCycle(duty)
        sleep(10)

    # servo
    def new_brake(self, duty):
        self.ser_1.ChangeDutyCycle(duty)
        #self.ser_2.ChangeDutyCycle(duty)

    def brakeon(self):
        """
        this method makes a crimer to brake on
        """
        self.ser_1.ChangeDutyCycle(self.brakeon_duty)
        #self.ser_2.ChangeDutyCycle(self.brakeon_duty)
        print("Brake on")
        sleep(.1)

    def brakeoff(self):
        """
        this method makes a crimer to brake off
        """
        self.ser_1.ChangeDutyCycle(self.brakeoff_duty)
        #self.ser_2.ChangeDutyCycle(self.brakeoff_duty)
        print("Brake off")

    def check_brake(self):
        while True:
            try:
              self.ser_1.ChangeDutyCycle(self.brakeoff_duty)
              print("Next ON.")
              sleep(1)
              self.ser_1.ChangeDutyCycle(self.brakeon_duty)
              print("Next OFF.")
              sleep(1)
            except KeyboardInterrupt:
              self.ser_1.ChangeDutyCycle(self.brakeoff_duty)
              sleep(1)
              print("Brake check completed.")
              break
              
    # tune mode, need to edit
    """
    def tune(self, meter):
        tuning_time = meter / self.tune_const_speed

        self.esc.ChangeDutyCycle(self.tune_const_duty)
        self.brakeoff()
        sleep(tuning_time)

        self.brakeon()
        self.esc.ChangeDutyCycle(0)
        sleep(1)
    """

    def end(self):
        """
        this method ends all the processes and clean up all pins 
        """
        print('デストラクタの呼び出し')
        del self.pin_esc
        del self.pin_servo_1 
        # del self.pin_servo_2
        del self.throttle_a0
        del self.throttle_a1
        del self.brakeon_duty
        del self.brakeoff_duty
        self.new_duty(0)
        # self.stop_esc()     
        self.brakeon()
        self.esc.stop()
        self.ser_1.stop()
        self.ser_2.stop()
        gpio.cleanup()

class Bme280:

    def __init__(self, address, bus_number=1):
        """
        address: address of bme280
        bus_number: 
        """
    
        self.bus = SMBus(bus_number)
        self.address = address

        self.digT = []
        self.digP = []
        self.digH = []
        self.t_fine = 0.0

        self.setup()
        self.get_calib_param()

    def get_calib_param(self):
		
        calib = []
		
        for i in range (0x88, 0x88+24):
            calib.append(self.bus.read_byte_data(self.address,i))
	    
        calib.append(self.bus.read_byte_data(self.address,0xA1))
	    
        for i in range (0xE1,0xE1+7):
            calib.append(self.bus.read_byte_data(self.address,i))

        self.digT.append((calib[1] << 8) | calib[0])
        self.digT.append((calib[3] << 8) | calib[2])
        self.digT.append((calib[5] << 8) | calib[4])
        self.digP.append((calib[7] << 8) | calib[6])
        self.digP.append((calib[9] << 8) | calib[8])
        self.digP.append((calib[11]<< 8) | calib[10])
        self.digP.append((calib[13]<< 8) | calib[12])
        self.digP.append((calib[15]<< 8) | calib[14])
        self.digP.append((calib[17]<< 8) | calib[16])
        self.digP.append((calib[19]<< 8) | calib[18])
        self.digP.append((calib[21]<< 8) | calib[20])
        self.digP.append((calib[23]<< 8) | calib[22])
        self.digH.append( calib[24] )
        self.digH.append((calib[26]<< 8) | calib[25])
        self.digH.append( calib[27] )
        self.digH.append((calib[28]<< 4) | (0x0F & calib[29]))
        self.digH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
        self.digH.append( calib[31] )

        for i in range(1, 2):
            if self.digT[i] & 0x8000:
                self.digT[i] = (-self.digT[i] ^ 0xFFFF) + 1

        for i in range(1, 8):
            if self.digP[i] & 0x8000:
                self.digP[i] = (-self.digP[i] ^ 0xFFFF) + 1

        for i in range(0, 6):
            if self.digH[i] & 0x8000:
                self.digH[i] = (-self.digH[i] ^ 0xFFFF) + 1  

    def compensate_P(self, adc_P):
        self.t_fine
        pressure = 0.0

        v1 = (self.t_fine / 2.0) - 64000.0
        v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * self.digP[5]
        v2 = v2 + ((v1 * self.digP[4]) * 2.0)
        v2 = (v2 / 4.0) + (self.digP[3] * 65536.0)
        v1 = (((self.digP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((self.digP[1] * v1) / 2.0)) / 262144
        v1 = ((32768 + v1) * self.digP[0]) / 32768
		
        if v1 == 0:
            return 0
        pressure = ((1048576 - adc_P) - (v2 / 4096)) * 3125
        if pressure < 0x80000000:
            pressure = (pressure * 2.0) / v1
        else:
            pressure = (pressure / v1) * 2
        v1 = (self.digP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
        v2 = ((pressure / 4.0) * self.digP[7]) / 8192.0
        pressure = pressure + ((v1 + v2 + self.digP[6]) / 16.0)  

        return pressure/100

    def compensate_T(self, adc_T):
        self.t_fine
        v1 = (adc_T / 16384.0 - self.digT[0] / 1024.0) * self.digT[1]
        v2 = (adc_T / 131072.0 - self.digT[0] / 8192.0) * (adc_T / 131072.0 - self.digT[0] / 8192.0) * self.digT[2]
        self.t_fine = v1 + v2
        temperature = self.t_fine / 5120.0
        return temperature 

    def compensate_H(self, adc_H):
        self.t_fine
        var_h = self.t_fine - 76800.0
        if var_h != 0:
            var_h = (adc_H - (self.digH[3] * 64.0 + self.digH[4]/16384.0 * var_h)) * (self.digH[1] / 65536.0 * (1.0 + self.digH[5] / 67108864.0 * var_h * (1.0 + self.digH[2] / 67108864.0 * var_h)))
        else:
            return 0
        var_h = var_h * (1.0 - self.digH[0] * var_h / 524288.0)
        if var_h > 100.0:
            var_h = 100.0
        elif var_h < 0.0:
            var_h = 0.0
        return var_h

    def writeReg(self, reg_address, data):
        self.bus.write_byte_data(self.address, reg_address, data)

    def setup(self):
        osrs_t = 1			#Temperature oversampling x 1
        osrs_p = 1			#Pressure oversampling x 1
        osrs_h = 1			#Humidity oversampling x 1
        mode   = 3			#Normal mode
        t_sb   = 5			#Tstandby 1000ms
        filter = 0			#Filter off
        spi3w_en = 0		#3-wire SPI Disable

        ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
        config_reg    = (t_sb << 5) | (filter << 2) | spi3w_en
        ctrl_hum_reg  = osrs_h

        self.writeReg(0xF2, ctrl_hum_reg)
        self.writeReg(0xF4, ctrl_meas_reg)
        self.writeReg(0xF5, config_reg)

    def read(self, name=False)->"return sensor data, (press, temp, humid)":
        """
        name: False -> only return tuple with data
              True  -> return dictionary with data and its name
        """
        data = []
        for i in range (0xF7, 0xF7+8):
            data.append(self.bus.read_byte_data(self.address,i))
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw  = (data[6] << 8)  |  data[7]

        data = self.compensate_P(pres_raw), self.compensate_T(temp_raw), self.compensate_H(hum_raw)

        if name == True:
            data_name = "press", "temp", "humid"
            data = dict(data_name, data)
            return data
        else:
            return data


class Sht31:

    def __init__(self, address, bus_number=1):
        """
        address: address of sht31
        bus_number: 
        """
        self.bus = SMBus(bus_number)
        self.address = address
        self.bus.write_byte_data(self.address, 0x23, 0x34)

    def tempChanger(self, msb, lsb):
        mlsb = ((msb << 8) | lsb)
        return 100 * int(str(mlsb), 10) / (pow(2, 16) - 1)

    def humidChanger(self, msb, lsb):
        mlsb = ((msb << 8) | lsb)
        return 100 * int(str(mlsb), 10) / (pow(2, 16) -1)

    def read(self, name=False)->"return sensor data, (temp, humid)":
        """
        name: False -> only return tuple with data
              True  -> return dictionary with data and its name
        """
        self.bus.write_byte_data(self.address, 0xE0, 0x00)
        data_raw = self.bus.read_i2c_block_data(self.address, 0x00, 6)
        data = self.tempChanger(data_raw[0], data_raw[1]), self.humidChanger(data_raw[3], data_raw[4])
        
        if name == True:
            data_name = "temp", "hunid"
            data = dict(data_name, data)
            return data
        else:
            return data


class Logger:
    
    def __init__(self, sensors:dict):
        self.sensors = sensors
        
        self.instances = {}
        for address, sensor in self.sensors.items():
            self.instances[address] = sensor(address)

    def reads(self):
        data = {}
        for address, instance in self.instances.items():
            data[address] = instance.read()

        return data


class Encoder:

    def __init__(self, pin_A, pin_B, diameter, resolution, goal):

        self.pin_A = pin_A
        self.pin_B = pin_B
        #self.pin_signal = pin_signal
        self.count = 0
        self.precount = 0
        self.sign = 0
        self.lastB = 0
        self.currentB = 0
        limit_rotation = int(goal * 1000 / (math.pi * diameter))    # diameter[mm]
        self.limit_pulse = limit_rotation * resolution

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin_A, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.pin_B, gpio.IN, pull_up_down=gpio.PUD_UP)
        #gpio.setup(self.pin_signal, gpio.OUT, initial=gpio.LOW)
        
        self.set_logfile()

        sleep(0.5)
        print(">> encoder setup is done.")
        print(">> limit_rotation:%d, limit_pulse = %d" % (limit_rotation, self.limit_pulse))
    
    def set_logfile(self):
        dt = datetime.datetime.now()
        location = "log"
        file_name = location + "encLog_" + str(dt.year) + "." + str(dt.month) + "." + str(dt.day + 4) + "_" + str(dt.hour + 20) + "." + str(dt.minute) + ".csv"
        self.f = open(file_name, "a")
        self.writer = csv.writer(self.f, lineterminator="\n")

        # datasize 2*20000
        self.log = [[0.0, 0]]
        for i in range(19999):
            self.log.append([0.0, 0])

    def deal(self):
        self.lastB = gpio.input(self.pin_B)

        while not(gpio.input(self.pin_A)):
            self.currentB = gpio.input(self.pin_B)
            self.sign = 1

        if self.sign == 1:
            ## Uprise or down fall judgement of B phase
            if self.lastB == 0 and self.currentB == 1:
                # CW
                self.count += 1
            if self.lastB == 1 and self.currentB == 0:
                # CCW
                self.count -= 1
            self.sign = 0

    def go(self):

        initial_time = time()
        now_time = time()
        goal_time = 0.0
        num = 0
        sig = 0

        while True:

            self.precount = self.count
            self.deal()

            # main for counting
            if self.precount != self.count:
                now_time = time() - initial_time
                self.log[num] = [now_time, self.count]
                print(self.count)
                num += 1

            # write data if no moving for 3 sec and num > 10000
            if (time() - initial_time > now_time + 3) and (num > 10000):
                print(">> writing data so far...")
                self.writer.writerows([i for i in self.log if not (i == [0.0, 0])])     # write data except element [0.0, 0]
                for i in range(20000):
                    self.log[i] = [0.0, 0]                                              # reset datalog
                print(">> ok, all done.")
                num = 0

            # output signal
            #if (sig == 0) and (self.count >= self.limit_pulse):
            #    gpio.output(self.pin_signal, gpio.HIGH)
            #    sig == 1
            #    goal_time = time() - initial_time

            # stop signal
            #if (sig == 1) and (time() - initial_time > goal_time + 3.0):
            #    gpio.output(self.pin_signal, gpio.LOW)

            if time() - initial_time > 30 * 60:
                break

    def end(self):
        self.writer.writerows([i for i in self.log if not (i == [0.0, 0])])
        gpio.cleanup([self.pin_A, self.pin_B])
        self.f.close()



class LS7366R():
    # Counter of Encoder
    #-------------------------------------------
    # Constants

    #   Commands
    CLEAR_COUNTER = 0x20
    CLEAR_STATUS = 0x30
    READ_COUNTER = 0x60
    READ_STATUS = 0x70
    WRITE_MODE0 = 0x88
    WRITE_MODE1 = 0x90

    #   Modes

    #May need to be change "QUADRATURE_COUNT_MODE" line depending on the quadrature count mode... look at datasheet.
    #These values are in HEX (base 16) whereas the data sheet displays them in binary.
    #Datasheet can be found here: https://www.lsicsi.com/pdfs/Data_Sheets/LS7366R.pdf

    #0x00: non-quadrature count mode. (A = clock, B = direction).
    #0x01: x1 quadrature count mode (one count per quadrature cycle).
    #0x02: x2 quadrature count mode (two counts per quadrature cycle).
    #0x03: x4 quadrature count mode (four counts per quadrature cycle).

    QUADRATURE_COUNT_MODE = 0x00


    FOURBYTE_COUNTER = 0x00
    THREEBYTE_COUNTER = 0x01
    TWOBYTE_COUNTER = 0x02
    ONEBYTE_COUNTER = 0x03

    BYTE_MODE = [ONEBYTE_COUNTER, TWOBYTE_COUNTER, THREEBYTE_COUNTER, FOURBYTE_COUNTER]
    PPR_ARRAY = [256, 512, 1024 , 2048]

    #   Values
    max_val = 4294967295
    
    # Global Variables

    counterSize = 4 #Default 4
    
    #----------------------------------------------
    # Constructor

    def __init__(self, CSX, CLK, BTMD, pin_RST, pin_INT):
        self.counterSize = BTMD #Sets the byte mode that will be used


        self.spi = spidev.SpiDev() #Initialize object
        self.spi.open(0, CSX) #Which CS line will be used
        self.spi.max_speed_hz = CLK #Speed of clk (modifies speed transaction)
        
        self.pin_RST = pin_RST
        self.pin_INT = pin_INT
        
        gpio.setmode(gpio.BCM) 
        gpio.setup(self.pin_RST, gpio.OUT, initial=gpio.HIGH) # reset pin needs to be HIGH to operate normally
        gpio.setup(self.pin_INT, gpio.OUT, initial=gpio.LOW)  # intervene pin is normally LOW if not consider external intervene
        

        #Init the Encoder
        print('Clearing Encoder CS%s\'s Count...\t' % (str(CSX)), self.clearCounter())
        print('Clearing Encoder CS%s\'s Status..\t' % (str(CSX)), self.clearStatus())

        self.spi.xfer2([self.WRITE_MODE0, self.QUADRATURE_COUNT_MODE])
        
        sleep(.1) #Rest
        
        self.spi.xfer2([self.WRITE_MODE1, self.BYTE_MODE[self.counterSize-1]])
        self.pulse_per_rotary = self.PPR_ARRAY[self.counterSize-1]


    def close(self):
        print('\nThanks for using me! :)')
        self.spi.close()

    def clearCounter(self):
        self.spi.xfer2([self.CLEAR_COUNTER])

        return '[DONE]'

    def clearStatus(self):
        self.spi.xfer2([self.CLEAR_STATUS])

        return '[DONE]'

    def readCounter(self):
        readTransaction = [self.READ_COUNTER]

        for i in range(self.counterSize):
            readTransaction.append(0)
            
        data = self.spi.xfer2(readTransaction)

        EncoderCount = 0
        for i in range(self.counterSize):
            EncoderCount = (EncoderCount << 8) + data[i+1]

        if data[1] != 255:    
            return EncoderCount
        else:
            return (EncoderCount - (self.max_val+1))
        
    def readRotaryRate(self):
        # translate pulse number into rotary rate
        # e.g.) If count is 2048, rotaryRate is 1.
        # Encoder counts 2048 pulse per one rotation if countersize = 4
        pulse = self.readCounter()
        rotaryRate = pulse / self.pulse_per_rotary
        
        return rotaryRate
        
        
    def readStatus(self):
        data = self.spi.xfer2([self.READ_STATUS, 0xFF])
        
        return data[1]


class E2S:
    def __init__(self, pin_e2s_top, pin_e2s_bottom): 
        """
        Argument
        ------------------------------------------
        pin_ec2top_ : ec2 corrector gpio
        pin_ec2_bottom : bottom ec2 corrector gpio 
        actu : actuator instance 
        """
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

        self.pin_e2s_top = pin_e2s_top
        self.pin_e2s_bottom = pin_e2s_bottom 
        gpio.setup(pin_e2s_top, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        gpio.setup(pin_e2s_bottom, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    
    def read_top(self): 
        top_sw_state = gpio.input(self.pin_e2s_top)
        return top_sw_state 

    def read_bottom(self): 
        bottom_sw_state = gpio.input(self.pin_e2s_bottom)
        return bottom_sw_state 

    def destroy(self): 
        gpio.cleanup()

class EM_SW:
    def __init__(self, pin_em_sw): 
        """
        Argument
        ------------------------------------------
        pin_em_sw : emergency switch signal gpio 
        """
        self.pin_em_sw = pin_em_sw
        gpio.setup(self.pin_em_sw, gpio.IN, gpio.PUD_UP) #switch is connected with pull-up  
    
    def read(self): 
        """switch not pressed => 1  switch pressed => 0"""
        em_sw_state = gpio.input(self.pin_em_sw)
        return em_sw_state   

    def destoy(self): 
        gpio.cleanup()
        sys.exit()

class TWILITE_REMOTE:
    def __init__(self, pin_remote_actuate, pin_remote_stop): 
        """
        Argument
        ------------------------------------------
        pin_remote_actuate_ : twilite signal for acutuating
        pin_remote_stop : twilite signal for stop 
        """
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

        self.pin_remote_actuate = pin_remote_actuate
        self.pin_remote_stop = pin_remote_stop 
        gpio.setup(pin_remote_actuate, gpio.IN)
        gpio.setup(pin_remote_stop, gpio.IN)
    
    def read_actuate(self): 
        actuate_signal = gpio.input(self.pin_remote_actuate)
        return actuate_signal 

    def read_stop(self): 
        stop_signal = gpio.input(self.pin_remote_stop)
        return stop_signal 

    def destroy(self): 
        gpio.cleanup()

