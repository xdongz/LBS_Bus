#coding:utf-8;
#qpy:2
#qpy:console

import time
import json
from urllib2 import urlopen
from androidhelper import Android

#lngx1=114.409661
#lngy1=30.47469
#lngx2=114.409567
#lngy2=30.476242
def distance(lngy1,lngx1,lngy2,lngx2):    
    ur='http://apis.map.qq.com/ws/distance/v1/?mode=driving&from='+str(lngy1)+','+str(lngx1)+'&to='+str(lngy2)+','+str(lngx2)+'&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
    f=urlopen(ur).read()
    f=json.loads(f)
    #print(f)
    #time.sleep(0.1)
    return(f[u'result'][u'elements'][0][u'distance'])
 
def start2huaxia_lanjing():
    ur='http://apis.map.qq.com/ws/distance/v1/?mode=driving&from=30.466851,114.393532&to=30.467499,114.408628;30.496725,114.416175&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
    f=urlopen(ur).read()
    f=json.loads(f)
    #print(f)
    #time.sleep(0.2)
    if f[u'result'][u'elements'][0][u'duration']>60:
        min1=f[u'result'][u'elements'][0][u'duration']/60
        duration1=str(min1)+'分钟'
    else:
        duration1=str(f[u'result'][u'elements'][0][u'duration'])+'秒'

    if f[u'result'][u'elements'][1][u'duration']>60:
        min2=f[u'result'][u'elements'][1][u'duration']/60
        duration2=str(min2)+'分钟'
    else:
        duration2=str(f[u'result'][u'elements'][1][u'duration'])+'秒'

    return(duration1,duration2) 
    
def huaxia2optical():
    ur='http://apis.map.qq.com/ws/distance/v1/?mode=driving&from=30.467499,114.408628&to=30.476242,114.409567&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
    f=urlopen(ur).read()
    f=json.loads(f)
    #print(f)
    #time.sleep(0.2)
    if f[u'result'][u'elements'][0][u'duration']>60:
        min1=f[u'result'][u'elements'][0][u'duration']/60
        duration1=str(min1)+'分钟'
    else:
        duration1=str(f[u'result'][u'elements'][0][u'duration'])+'秒'

    return duration1  

def optical2xinzhu():
    ur='http://apis.map.qq.com/ws/distance/v1/?mode=driving&from=30.476242,114.409567&to=30.489422,114.411117&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
    f=urlopen(ur).read()
    f=json.loads(f)
    #print(f)
    #time.sleep(0.2)
    if f[u'result'][u'elements'][0][u'duration']>60:
        min1=f[u'result'][u'elements'][0][u'duration']/60
        duration1=str(min1)+'分钟'
    else:
        duration1=str(f[u'result'][u'elements'][0][u'duration'])+'秒'

    return duration1

def xinnan2lanjing():
    ur='http://apis.map.qq.com/ws/distance/v1/?mode=driving&from=30.492301,114.411407&to=30.496725,114.416175&key=Y5YBZ-VLZCX-EQR4Y-Z47JH-TZCHQ-TXF7H'
    f=urlopen(ur).read()
    f=json.loads(f)
    #print(f)
    #time.sleep(0.2)
    if f[u'result'][u'elements'][0][u'duration']>60:
        min1=f[u'result'][u'elements'][0][u'duration']/60
        duration1=str(min1)+'分钟'
    else:
        duration1=str(f[u'result'][u'elements'][0][u'duration'])+'秒'

    return duration1