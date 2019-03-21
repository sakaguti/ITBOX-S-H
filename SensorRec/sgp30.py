#!/usr/bin/env python3
""" Example for using the SGP30 with CircuitPython and the Adafruit library"""

import time
import datetime
import sys
import os
import os.path
import subprocess
import threading
import board
import busio
import adafruit_sgp30

timeupTime=30

# write every 1 h
writeTime=60
#writeTime=1

#samplint data by 10sec
samplingTime=10

id='TVOC'
ID=id
Year=''
Month=''
Day=''
Hour=''
Min=''
dataBuffer=''
#
pathdir='/mnt/SensorsData/'
latestFile='/mnt/SensorsData/'+id+'/saveSGP30data.csv'
#

class appendLoalFile(threading.Thread):
        def __init__(self,filename,dataBuffer):
                threading.Thread.__init__(self)
                self.filename=filename
                self.dataBuffer=str(dataBuffer)

        def run(self):
                f = open(self.filename, 'a')
                f.write(self.dataBuffer)
                f.close()

def timeDateFormat(now):
        mon=str(getattr(now,'month'))
        if len(mon) == 1:
                mon = '0'+mon;
        day=str(getattr(now,'day'))
        if len(day) == 1:
                day = '0'+day;
        hour=str(getattr(now,'hour'))
        if len(hour) == 1:
                hour = '0'+hour;
        min=str(getattr(now,'minute'))
        if len(min) == 1:
                min = '0'+min;
        sec=str(getattr(now,'second'))
        if len(sec) == 1:
                sec = '0'+sec;
        year=str(getattr(now,'year'))
        return year,mon,day,hour,min,sec

def makeDir(id,year,month,day,hour,min):
        global ID
        global Year
        global Month
        global Day
        global Hour
        global Min

        os.chdir(pathdir)
        if ID != id and id !='':
                ID=id
                dir =id+'/'
                if os.path.exists(dir) == False:
                        # make dir
                        try:
                                os.makedirs(dir)
                                print('Mkdir ',dir )
                        except:
                                print('Mkdir year Error ',dir )
                                return None
        if Year != year and year !='':
                Year=year
                dir =id+'/'+year+'/'
                if os.path.exists(dir) == False:
                        # make dir
                        try:
                                os.makedirs(dir)
                                print('Mkdir ',dir )
                        except:
                                print('Mkdir year Error ',dir )
                                return None
        if Month != month and month != '':
                Month=month
                dir =id+'/'+year+'/'+month+'/'
                if os.path.exists(dir) == False:
                        # make dir
                        try:
                                os.makedirs(dir)
                                print('Mkdir ',dir )
                        except:
                                print('Mkdir month Error ',dir )
                                return None
        if Day != day and day != '':
                Day=day
                dir =id+'/'+year+'/'+month+'/'+day+'/'
                if os.path.exists(dir) == False:
                        # make dir
                        try:
                                os.makedirs(dir)
                                print('Mkdir ',dir )

                        except:
                                print('Mkdir day Error ',dir )
                                return None
        if Hour != hour and hour != '':
                Hour=hour
                dir =id+'/'+year+'/'+month+'/'+day+'/'+hour+'/'
                if os.path.exists(dir) == False:
                        # make dir
                        try:
                                os.makedirs(dir)
                                print('Mkdir ',dir )
                        except:
                                print('Mkdir hour Error ',dir )
                                return None
        if Min != min and min != '':
                Min=min
                dir =id+'/'+year+'/'+month+'/'+day+'/'+hour+'/'+min+'/'
                if os.path.exists(dir) == False:
                        # make dir
                        try:
                                os.makedirs(dir)
                                print('Mkdir ',dir )
                        except:
                                print('Mkdir min Error ',dir )
                                return None



i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

if __name__ == '__main__':
    sgp30.iaq_init()
    sgp30.set_iaq_baseline(0x8973, 0x8aae)

    while True:
        start = datetime.datetime.now()
        linedata = ''
        co2eq = sgp30.co2eq 
        tvoc  = sgp30.tvoc
        linedata = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +',CO2,'+str(co2eq)+',TVOC,'+str(tvoc)+'\n'
        #sys.stdout.write(linedata)

        if int(start.second) % 10 == 0:

            #print("**** Baseline values: co2eq = 0x%x, tvoc = 0x%x"
            #      % (sgp30.baseline_co2eq, sgp30.baseline_tvoc))

            dataBuffer = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +',CO2,'+str(co2eq)+',TVOC,'+str(tvoc)+',CO2EQ_BASELINE,'+str(sgp30.baseline_co2eq)+',TVOC_BASELINE,'+str(sgp30.baseline_tvoc)+'\n'

            # save dataBuffer data
            now = datetime.datetime.now()
            year,mon,day,hour,min,sec=timeDateFormat(now)
            dir=id+'/'+str(year)+'/'+str(mon)+'/'+str(day)+'/'
            makeDir(id,year,mon,day,'','')
            filename=str(year)+'-'+str(mon)+'-'+str(day)+'_'+str(hour)+'.csv'

            sys.stdout.write(dir+filename+' '+ dataBuffer)

            if len(dataBuffer) > 0:
            # save to local file
                filename=dir+filename
                appendLoalFile(filename,dataBuffer).start()
                if int(start.minute) == 0:
                    # remove file
                    os.remove(latestFile)
                    #
                appendLoalFile(latestFile,dataBuffer).start()

        now = datetime.datetime.now()
        time.sleep(1.0-float(str(now-start).replace('0:00:0','')))
