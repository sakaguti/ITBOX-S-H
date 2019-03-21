#!/usr/bin/env python3

from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
import datetime
import sys
import board
import busio
import adafruit_sgp30
import thingspeak

pause = 10 

channel_id = 558443
write_key = 'MDRUFR8SV9RW6UZ1' # PUT YOUR WRITE KEY HERE

fd = open('/home/pi/data/ccs811andsgp30log.txt', 'a')

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
print("SGP30 serial #", [hex(i) for i in sgp30.serial])

ccs =  Adafruit_CCS811(mode=0x01, address=0x5a, i2c=None)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)
elapsed_sec = 0
channel = thingspeak.Channel(id=channel_id,write_key=write_key)


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
           co2eq = sgp30.co2eq
           tvoc  = sgp30.tvoc
        except:
            print('SGP30 Error01')
            sleep(1)
            continue

        try:
            temp = ccs.calculateTemperature()
            available=ccs.available()
            readData=ccs.readData()
        except:
            print('CCS811 Error01')
            sleep(1)
            continue

        if available == False or readData < 16:
            print('CCS811 Error02 available=',available,'readData = ',readData)
            sleep(1)
            continue

        try:
            CO2=ccs.geteCO2()
            TVOC=ccs.getTVOC()
        except:
            print('CCS811 Error03')
            sleep(1)
            continue

        linedata = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +',CCS811 , CO2, '+str(CO2)+', TVOC ,'+str(TVOC)+', temp ,'+str(temp)+', SGP30 , eCO2 ,'+str(co2eq)+', TVOC ,'+str(tvoc)

        print(linedata)
        linedata += '\n'
        fd.write(linedata)
        fd.flush()

        try:
            sponse = channel.update({1:TVOC, 2:CO2, 3:tvoc, 4:co2eq})
        except:
            print( "WiFi connection failed. Can not updload to ThingSpeak.")
            continue

        sleep(pause)
