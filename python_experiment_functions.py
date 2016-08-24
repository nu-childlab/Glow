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
from psychopy import visual,logging,event,core

def instructions_screen(win, scrwidth, scrheight, txt):
	background = visual.Rect(win,lineWidth=0,fillColor="black",size=[scrwidth,scrheight],pos=[0,0],
	units="height")
	#Cover up the background with black; the square should be the same size as the window
	welcomeText = visual.TextStim(win,text='Welcome to the experiment!',
		height=40, color='white',pos=[0,0], wrapWidth=scrwidth/3)
	descriptionText = visual.TextStim(win,text=txt,
		height=20, color='white',pos=[0,0], wrapWidth=scrwidth/3)
	promptText = visual.TextStim(win,text='Press spacebar to continue',
		height=40, color='white',pos=[0,-40], wrapWidth=scrwidth/3)
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


def subjectCheck(subject):
	if re.search("^s\d*$", subject):
		return subject
	else:
		print "Invalid subject id! An id should be an 's' followed by only numbers."
		return subjectCheck(input("Please enter a valid subject id: "))
