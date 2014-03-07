#!/usr/bin/env python2.7
#PiCamera Video Synth via OSC version 0.1

#Import libraries

#import RPi.GPIO as GPIO
import time
import picamera
import random
import socket
import OSC
import threading
import os, sys
import pipan

#Define variables

brightness = 50
contrast = 0
saturation = 0
colorfxone = 128
colorfxtwo = 128
rotation = 180
sharpness = 0
cropx = 0.0
cropy = 0.0
cropw = 1.0
croph = 1.0
imgfx1 = 'none'
exposure = 'auto'
awb = 'auto'
onoff = 0
quit = 0
tilt = 150
pan =  150
alpha = 255
prex = 0
prey = 0
prewidth = 1920
preheight = 1080
fs = False
colortog = 0
moviename = 'test.h264'
movieplay = 0

global camera

#Setup the OSC Server's IP Address

receive_address = '0.0.0.0', 9000
s = OSC.OSCServer(receive_address)
s.addDefaultHandlers()

#client_socket = socket.socket()
#client_socket.connect(('10.0.1.5', 8000))

# Make a file-like object out of the connection
#connection = client_socket.makefile('wb')

#Define the functions for incoming OSC messages

def movieplay_handler(addr, tags, stuff, source):
    global movieplay
    movieplay=str(stuff)[1:-1]

def moviename_handler(addr, tags, stuff, source):
    global moviename
    moviename=str(stuff)[1:-1]

def colortog_handler(addr, tags, stuff, source):
    global colortog
    colortog=str(stuff)[1:-1]

def alpha_handler(addr, tags, stuff, source):
    global alpha
    alpha=str(stuff)[1:-1]

def fullscreen_handler(addr, tags, stuff, source):
    global fs
    fs=str(stuff)[2:-2]
    print fs

def prex_handler(addr,tags, stuff, source):
    global prex
    prex=str(stuff)[1:-1]

def prey_handler(addr, tags, stuff, source):
    global prey
    prey=str(stuff)[1:-1]

def prewidth_handler(addr, tags, stuff, source):
    global prewidth
    prewidth=str(stuff)[1:-1]

def preheight_handler(addr, tags, stuff, srouce):
    global preheight
    preheight=str(stuff)[1:-1]

def pan_handler(addr, tags, stuff, source):
    global pan
    pan=str(stuff)[1:-1]

def tilt_handler(addr, tags, stuff, source):
    global tilt
    tilt=str(stuff)[1:-1]

def neutral_handler(addr, tags, stuff, source):
    global neutral
    neutral=str(stuff)[1:-1]

def quit_handler(addr, tags, stuff, source):
    global quit
    quit=str(stuff)[1:-1]

def brightness_handler(addr, tags, stuff, source):    
    global brightness
    brightness=str(stuff)[1:-1]

def contrast_handler(addr, tags, stuff, source):
    global contrast
    contrast=str(stuff)[1:-1]
 
def saturation_handler(addr, tags, stuff, source):
    global saturation
    saturation=str(stuff)[1:-1]

def colorfxone_handler(addr, tags, stuff, source):
    global colorfxone
    colorfxone=str(stuff)[1:-1]

def colorfxtwo_handler(addr, tags, stuff, source):
    global colorfxtwo
    colorfxtwo=str(stuff)[1:-1]

def rotation_handler(addr, tags, stuff, source):
    global rotation
    rotation=str(stuff)[1:-1]

def sharpness_handler(addr, tags, stuff, source):
    global sharpness
    sharpness=str(stuff)[1:-1]

def cropx_handler(addr, tags, stuff, source):
    global cropx
    cropx=str(stuff)[1:-1]

def cropy_handler(addr, tags, stuff, source):
    global cropy
    cropy=str(stuff)[1:-1]

def cropw_handler(addr, tags, stuff, source):
    global cropw
    cropw=str(stuff)[1:-1]

def croph_handler(addr, tags, stuff, source):
    global croph
    croph=str(stuff)[1:-1]

def imgfx1_handler(addr, tags, stuff, source):
    global imgfx1
    imgfx1=str(stuff)[2:-2]

def exposure_handler(addr, tags, stuff, source):
    global exposure
    exposure=str(stuff)[2:-2]

def awb_handler(addr, tags, stuff, source):
    global awb
    awb=str(stuff)[2:-2]

def onoff_handler(addr, tags, stuff, source):
    global onoff
    onoff=str(stuff)[1:-1]
    print(onoff)

# Call the functions handling incoming OSC messages

s.addMsgHandler("/movieplay", movieplay_handler)
s.addMsgHandler("/moviename", moviename_handler)
s.addMsgHandler("/colortog", colortog_handler)
s.addMsgHandler("/prex", prex_handler)
s.addMsgHandler("/prey", prey_handler)
s.addMsgHandler("/prewidth", prewidth_handler)
s.addMsgHandler("/preheight", preheight_handler)
s.addMsgHandler("/fullscreen", fullscreen_handler) 
s.addMsgHandler("/alpha", alpha_handler)
s.addMsgHandler("/pan", pan_handler)
s.addMsgHandler("/tilt", tilt_handler)
s.addMsgHandler("/neutral", neutral_handler)
s.addMsgHandler("/quit", quit_handler)
s.addMsgHandler("/brightness", brightness_handler)
s.addMsgHandler("/contrast", contrast_handler)
s.addMsgHandler("/saturation", saturation_handler)   
s.addMsgHandler("/colorfxone", colorfxone_handler)
s.addMsgHandler("/colorfxtwo", colorfxtwo_handler)
s.addMsgHandler("/rotation", rotation_handler)
s.addMsgHandler("/sharpness", sharpness_handler)
s.addMsgHandler("/cropx", cropx_handler)
s.addMsgHandler("/cropy", cropy_handler)
s.addMsgHandler("/cropw", cropw_handler)
s.addMsgHandler("/croph", croph_handler)
s.addMsgHandler("/imgfx1", imgfx1_handler)
s.addMsgHandler("/exposure", exposure_handler)
s.addMsgHandler("/awb", awb_handler)
s.addMsgHandler("/onoff", onoff_handler)

# Define the responses to command line input options

arguments = sys.argv[1:]
count = len(arguments)
runtime = 2300

if int(count) == 0:
   print "The runtime is 30 seconds"
   #time.sleep(2)

elif int(count) == 1:
   input_one =sys.argv[1]
   runtime = int(input_one) * 76
   print "The runtime is %s seconds" % input_one

elif int(count) == 2:
   input_one = sys.argv[1] 
   print "The runtime is %s seconds" % input_one
   runtime = int(input_one) * 76
   record_filename = sys.argv[2]
   print "Recording to a file named" %s, record_filename

#Start the OSC Server
   
st = threading.Thread(target = s.serve_forever)
st.start()
print "The OSC Server is ON"

#Turn on the Pi Camera

camera = picamera.PiCamera()
camera.start_preview()
print "The Camera is ON"

#camera.start_recording(connection, format='h264')
print "Sending stream"

#Pi-Pan Parameters

print "Set the Camera to pan & tilt neutral"
p = pipan.PiPan()
p.neutral_pan()
p.neutral_tilt()

#Start recording if indicated on startup

if int(count) == 2:
    camera.start_recording(str(record_filename))
    print "Recording has started"

# Freak out!
print "#############################"
print "FREAK OUT !!!!!!"
print "#############################"

try:
    for i in range (int(runtime)):
        #if int(quit) == 1:
            #print "Quit is 1"
            #break
	camera.preview_window = (int(prex),int(prey),int(prewidth),int(preheight))
	camera.preview_fullscreen = fs
        camera.image_effect = imgfx1
        camera.brightness = int(brightness)
	camera.contrast = int(contrast)
        camera.saturation = int(saturation)
        if int(colortog) == 1:
            camera.color_effects = (int(colorfxone),int(colorfxtwo))
        if int(colortog) == 0:
            camera.color_effects == 'none'
        if int(movieplay) == 1:
            os.system('omxplayer -o hdmi test.h264')
            movieplay == 0
            print movieplay
        camera.exposure_mode = exposure
        camera.awb_mode = awb
        camera.rotation = int(rotation)
        camera.sharpness = int(sharpness)
        camera.crop = (float(cropx),float(cropy),float(cropw),float(croph))
        camera.preview_alpha = int(alpha)
        p.do_tilt (int(tilt))
        p.do_pan (int(pan))
       # time.sleep(0.1)       
finally: 
    if int(count) == 2:
	print "The runtime is 0"
        camera.stop_recording()
        print "The Recording has stopped,"
        camera.stop_preview()
        print "The Camera is OFF"
        s.close()
        st.join()
        print "The OSC Server is OFF"
    else:
        print "The runtime is now 0"
        #camera.stop_recording()
        camera.stop_preview()
        print "The Camera is OFF"
        s.close()
        st.join()
        #connection.close()
        #client_socket.close()
        print "The OSC Server is OFF"


