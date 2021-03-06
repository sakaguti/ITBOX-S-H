#!/usr/bin/python
# -*- coding: utf-8 -*-#
#
# Sensor Recording
#		data from sensors by every one second. save it to file which file name is data/year/month/day
#		save data every by 1 hour, filename is Sensor/year/month/day/year-month-day_hour.csv.
#
#		copyright Aug.2017   itplants,ltd.
#
#
import datetime
import serial
import time
import sys
import glob
import os
import threading
import os.path
import traceback

timeupTime=30

SENSOR='CO2'
# for test of itplants
testSW=False
#

verbosSW=True
#verbosSW=False
readSW=True
bufsize=2048

# write every 1 h 
writeTime=60
#writeTime=1

#samplint data by 10sec
samplingTime=10

ID=''
Year=''
Month=''
Day=''
Hour=''
Min=''
#
pathdir='/mnt/SensorsData/'
#

class dataRec:
	# Data Recorder Control
	def __init__(self):
		self.status=False
		# search /dev/ttySOFT*  or /dev/cu.*usb*
		devfile=None
		devfile=glob.glob('/dev/ttySOFT?')
		if len(devfile) == 0:
			devfile=glob.glob('/dev/cu.usbserial')

		# Mac/RPI
		self.ser= serial.Serial(devfile[0], 9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.3)
                if self.ser == '':
		    print('device open error')
                    sys.exit(0)

	def read(self):
		#s = self.ser.read(bufsize)
		#s = self.ser.readline()
		b=''
		try:
			while True:
				s = self.ser.read()
				b += s
				if s == '\n':
					break
		except KeyboardInterrupt:
			print('keyboard Interrupt')
			os._exit(0)
		except :
                        traceback.print_exc()

		b = b.replace('\r','')
		b = b.replace('\n','')
		return b

class appendLoalFile(threading.Thread):
	def __init__(self,filename,dataBuffer):
		threading.Thread.__init__(self)
		self.filename=filename
		self.dataBuffer=str(dataBuffer)

	def run(self):
		f = open(self.filename, 'a')
       		f.write(self.dataBuffer)
                f.flush()
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

        os.chdir('/mnt/SensorsData/')
	if ID != id and id !='':
		ID=id
		dir =pathdir
		if os.path.exists(dir) == False:
			# make dir
			try:
			        os.makedirs(dir)
				print('Mkdir ',dir )
			except:
                                traceback.print_exc()
				print('Mkdir year Error ',dir )
				return None
	if Year != year and year !='':
		Year=year
		dir =pathdir+year+'/'
		if os.path.exists(dir) == False:
			# make dir
			try:
				os.makedirs(dir)
				print('Mkdir ',dir )
			except:
                                traceback.print_exc()
				print('Mkdir year Error ',dir )
				return None
	if Month != month and month != '':
		Month=month
		dir =pathdir+year+'/'+month+'/'
		if os.path.exists(dir) == False:
			# make dir
			try:
				os.makedirs(dir)
			except:
                                traceback.print_exc()
				print('Mkdir month Error ',dir )
				return None
	if Day != day and day != '':
		Day=day
		dir =pathdir+year+'/'+month+'/'+day+'/'
		if os.path.exists(dir) == False:
			# make dir
			try:
				os.makedirs(dir)
				print('Mkdir ',dir )
			except:
                                traceback.print_exc()
				print('Mkdir day Error ',dir )
				return None
	if Hour != hour and hour != '':
		Hour=hour
		dir =pathdir+year+'/'+month+'/'+day+'/'+hour+'/'
		if os.path.exists(dir) == False:
			# make dir
			try:
				os.makedirs(dir)
				print('Mkdir ',dir )
			except:
                                traceback.print_exc()
				print('Mkdir hour Error ',dir )
				return None
	if Min != min and min != '':
		Min=min
		dir =pathdir+year+'/'+month+'/'+day+'/'+hour+'/'+min+'/'
		if os.path.exists(dir) == False:
			# make dir
			try:
				os.makedirs(dir)
				print('Mkdir ',dir )
			except:
                                traceback.print_exc()
				print('Mkdir min Error ',dir )
				return None

if __name__ == '__main__':
	id=SENSOR
	year=''
	month=''
	day=''
        hour=''
        dataBuffer=''
	#
        os.chdir(pathdir)
	# recoder every one sec
	secRec=False
	#

	args = sys.argv
	i=0
	for arg in args:
		if arg=='-recsec':
			secRec=True 
		if arg=='-wtime':
			writeTime=int(args[i+1])
		if arg=='-id':
			id=args[i+1]
		if arg=='-h' or arg=='-help':
			print(args[0])
			print(        ' -recsec : recode file by every sec. default False')
			print(        ' -id [X02] :  ID of datalogger. default X02')
			print(        ' -wtime min : recode file by every min. default 15min')
			print(        ' -h  : display help')
			sys.exit()
		i += 1

        pathdir=pathdir+id+'/' 
        latestFile=pathdir+'saveCO2data.csv'

        try:
	    prj=dataRec()
 	    data=prj.read()
	except :
	    print('Data Sensor ERROR\n')
            traceback.print_exc()
            time.sleep(2)

	ID=id
	Year=year
	Month=month
	Day=day
	Hour=hour
	Min=min

        nerror = 0
        data=''
        try:
	        while True:
			start = datetime.datetime.now()

			try:
				data=prj.read()
                                #print(data)
			except:
                                traceback.print_exc()
				print('Data Read Error:',nerror)
                        	nerror += 1
                                time.sleep(2)
				continue
                        if len(data) != len('2018-10-01 13:02:00,Z,00455,z,00439'):
                                time.sleep(0.2) 
                                continue 

			data=data.replace(' ',',')
                        #data=data[1:]
			data = "{0:%Y-%m-%d %H:%M:%S}".format(start)+','+data[1:]+'\n'
			if len(data) != 36:
				# datalogger power OFF
	                        print('Data Sensor ERROR  length='+str(len(data)))
	                        print(data)
				time.sleep(1)
				continue

                	if nerror >= timeupTime:
                        	data='ERROR can not read data from datalogger.'
                        	sys.stderr.write('['+str(nerror)+'] ')
                        	sys.stderr.write('data Error:')
                        	sys.stderr.write(data+'\n')
                        	sys.stderr.flush()
                        	# write log file
				os._exit()

			###
	  		year,mon,day,hour,min,sec=timeDateFormat(start)

			# append
			#print('sec='+str(int(sec) % samplingTime))
			if int(sec) % int(samplingTime) == 0:
				makeDir(id,year,mon,day,'','')
				# save data
				dir=pathdir+year+'/'+mon+'/'+day+'/'
				filename=year+'-'+mon+'-'+day+'_'+hour+'.csv'
				print('saved '+dir+filename,' data ', data)
				if len(data) > 0:
					# save to local file
					filename=dir+filename
			 		appendLoalFile(filename,data).start()
			                if int(min) == 0:
                                            try:
                                                os.remove(latestFile)
                                            except:
                                                traceback.print_exc()
				        #print('saved '+latestFile,' data ', data)
			 		appendLoalFile(latestFile,data).start()
                                        time.sleep(0.2)
				
                        	nerror = 0

		now = datetime.datetime.now()
                time.sleep(1.0-float(str(now-start).replace('0:00:0','')))

	except KeyboardInterrupt:
		print('keyboard Interrupt')
		os._exit()
        except:
                traceback.print_exc()
