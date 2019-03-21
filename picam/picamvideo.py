#!/usr/bin/env python
import picamera
import sys
import os
import datetime as dt
import datetime

import subprocess
#subprocess.call( ["./sysctl.sh", "stop"] ) 

filename = dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

camera = picamera.PiCamera(resolution=(1280, 720), framerate=24)
#camera.start_preview()
print('start rec')
camera.annotate_background = picamera.Color('black')

camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.start_recording(filename+'.h264')

start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 30:
    #print( str(30-((dt.datetime.now() - start).seconds))+' '),
    sys.stdout.write( str(30-int((dt.datetime.now() - start).seconds))+' ')
    sys.stdout.flush()
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.wait_recording(0.2)
camera.stop_recording()
print('end rec')
#subprocess.call( ["./sysctl.sh", "start"] ) 
