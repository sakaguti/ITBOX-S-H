#!/usr/bin/python
#this example reads and prints CO2 equiv. measurement, TVOC measurement, and temp every 2 seconds

from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
import datetime
import sys
import urllib2 
#import BME280 as bme280

fd = open('/home/pi/data/ccs811log.txt', 'a')

THINGSPEAK      = '12Y6WDEM3B3HMX7O' #False # or type 'YOURAPIKEY'
pause = 3

def thingSpeak(eCO2,TVOC,Temp):
    print 'Sending to ThingSpeak API...'
    url = "https://api.thingspeak.com/update?api_key="
    url += THINGSPEAK
    url += "&field1="
    url += str(eCO2)
    url += "&field2="
    url += str(TVOC)
    url += "&field3="
    url += str(Temp)
    print( url )
    try: 
      content = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
      print "Invalid HTTP response"
      return False
    print( 'Done')

ccs =  Adafruit_CCS811(mode=0x01, address=0x5a, i2c=None)

while not ccs.available():
	pass

try:
        temp = ccs.calculateTemperature()
        ccs.tempOffset = temp - 25.0
        print( 'ccs.tempOffset=',ccs.tempOffset )
except:
        print( "ERROR! 00")

while(1):
        linedata=''
        try:
	    temp = ccs.calculateTemperature()
	    available=ccs.available()
	    readData=ccs.readData()
        except:
            print('Error01')
            sleep(1) 
            continue

        if available == False or readData < 16:
            print('Error02 available=',available,'readData = ',readData)
            sleep(1) 
            continue

        try:
            CO2=ccs.geteCO2()
            TVOC=ccs.getTVOC()
        except:
            print('Error03')
            sleep(1) 
            continue

        #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" CO2: "+str( CO2)+ "ppm  TVOC: "+str( TVOC )+" ppg  temp: "+str( temp )+' deg')

        linedata = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +',CO2,'+str(CO2)+',TVOC,'+str(TVOC)+',temp,'+str(temp)+'\n'

        print(linedata)
        fd.write(linedata)
        fd.flush()

        try:
            thingSpeak(CO2,TVOC,temp)
        except:
            print('Thigspeak Error')
            pass

	sleep(pause)
