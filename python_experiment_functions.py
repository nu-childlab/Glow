from __future__ import division
import matplotlib
import pylab
import time
import sys
import random
import re
import csv
import math
import numpy as np
from psychopy import visual,logging,event,core, monitors

def window_creation(fullscreen, background_color):
	if fullscreen:
		m = monitors.Monitor(monitors.getAllMonitors()[0])
		win = visual.Window(units='pix', monitor=m, color=background_color, colorSpace="rgb255", fullscr=True)
		wsize = win.size
		scrwidth = wsize[0]
		scrheight = wsize[1]
	else:
		scrwidth = 1280
		scrheight = 720
		win = visual.Window([scrwidth,scrheight], units='pix', monitor='testMonitor', color=background_color, colorSpace="rgb255")
	return win, scrwidth, scrheight

def instructions_screen(win, scrwidth, scrheight, txt):
	background = visual.Rect(win,lineWidth=0,fillColor="black",size=[scrwidth,scrheight],pos=[0,0],
	units="height")
	#Cover up the background with black; the square should be the same size as the window
	welcomeText = visual.TextStim(win,text='Welcome to the experiment!',
		height=40, color='white',pos=[0,scrheight/3], wrapWidth=scrwidth/2)
	descriptionText = visual.TextStim(win,text=txt,
		height=30, color='white',pos=[0,0], wrapWidth=scrwidth/2)
	promptText = visual.TextStim(win,text='Press spacebar to continue',
		height=40, color='white',pos=[0,-scrheight/3], wrapWidth=scrwidth/2)
	background.draw()
	welcomeText.draw()
	descriptionText.draw()
	promptText.draw()
	#Create the text, then draw it.
	win.flip()
	while True:
		response=event.waitKeys(keyList=['space'])[0]
		break

def response_screen(win, scrwidth, scrheight, question, prompt, keys):
	timer = core.Clock()
	background = visual.Rect(win,lineWidth=0,fillColor="black",size=[scrwidth,scrheight],pos=[0,0],
	units="height")
	#Cover up the background with black; the square should be the same size as the window
	responseText = visual.TextStim(win,text=question,
		height=40, color='white',pos=[0,0], wrapWidth=scrwidth/3)
	promptText = visual.TextStim(win,text=prompt,
		height=20, color='white',pos=[0,-120], wrapWidth=scrwidth/3)
	background.draw()
	responseText.draw()
	promptText.draw()
	#Create the text, then draw it.
	win.flip()
	timer.reset()
	#start the timer
	while True:
		response=event.waitKeys(keyList=keys)[0]
		break
		#Wait for a response, and leave the loop when you have it
	rt = timer.getTime()
	return [response, rt]

def finish_screen(win, scrwidth, scrheight):
	background = visual.Rect(win,lineWidth=0,fillColor="black",size=[scrwidth,scrheight],pos=[0,0],
	units="height")
	#Cover up the background with black; the square should be the same size as the window
	finishText = visual.TextStim(win,text='Thanks for participating!',
		height=40, color='white',pos=[0,0], wrapWidth=scrwidth/2)
	background.draw()
	finishText.draw()
	#Create the text, then draw it.
	win.flip()
	while True:
		response=event.waitKeys(keyList=['escape'])[0]
		break

def getSubjectId():
	subject = str(raw_input("Subject Number: "))
	while True:
		if re.search("^s\d+$", subject):
			break
		else:
			print "Invalid subject id! An id should be an 's' followed by only numbers."
			subject = str(raw_input("Please enter a valid subject id: "))

	return subject
