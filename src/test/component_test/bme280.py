import selemod
import time 

bme = selemod.Bme280(0x76)

# bme280 
c = 0
total_num = 10
print('BME280')
while(c<total_num):
    press, temp, humid = bme.read()
    print('\n-------------------')
    print('[data : %d/%d]' %(c+1, total_num))
    print('pressure : %.3f' % press)
    print('temp : %.4f' % temp)
    print('humid : %.4f' % humid)
    c+=1
    # time.sleep(1)