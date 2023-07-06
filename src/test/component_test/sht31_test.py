import selemod
import time 
sht = selemod.Sht31(0x45)
# sht31 
c = 0
total_num = 10 
while(c<total_num):
    temp, humid = sht.read()
    print('\nSHT31')
    print('\n-------------------')
    print('[data : %d/%d]' %(c+1, total_num))
    print('temp : %.4f' % temp)
    print('humid : %.4f' % humid)
    c+=1
    # time.sleep(1)