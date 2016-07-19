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
from color_functions import *
from shape_manager import shape_Manager

def main():

	# subject = str(raw_input("Subject Number: "))
	# subject = subjectCheck(subject)
	# print subject

	#2560, 1440
	#1280, 720
	scrwidth = 960
	scrheight = 540
	#the length of the square's sides; the other shapes are calculated to fit within the square.
	#the length of the square = the diameter of the circle = the base and height of the triangle.
	sqsize = scrwidth/5
	#The positions are from the center of the screen, and mirror each other.
	pos1 = -scrwidth/5
	pos2 = -pos1
	background_color = [175,175,175]

	win = visual.Window([scrwidth,scrheight], units='pix', monitor='testMonitor', color=[175,175,175], colorSpace="rgb255")

	framerate = win.getActualFrameRate()

	#ifi = .0169
	ifi = 1/framerate

	# read parameters file and open response file below
	parametersfile = open('glowparameters.csv', 'rU')
	parametersreader = csv.DictReader(parametersfile)
	# responsefile = open('glowresponses.csv', 'wb')
	# responsefields = ['Response', 'RT']
	# responsewriter = csv.DictWriter(responsefile, responsefields)
	# responsewriter.writeheader()

	#create a timer
	timer = core.Clock()

	#parameters: Left Shape,Left Start Color, Left End Color,Left Glow,Left Variable 1,
	#L1 time/rate/number,Left Variable 2,L2 time/rate/number,Right Shape,Right Start Color,Right End Color,
	#Right Glow,Right Variable 1,R1 value type,Right Variable 2,R2 value type



	parameters = []
	for row in parametersreader:
	 	parameters.append(row)

	random.shuffle(parameters)
	rowcount = 2
	sm = shape_Manager(win, sqsize, pos1, pos2, background_color)

	for row in parameters:
		left_shape = row["Left Shape"]
		left_start_color = row["Left Start Color"]
		left_end_color = row["Left End Color"]
		left_glow = row["Left Glow"]

		right_shape = row["Right Shape"]
		right_start_color = row["Right Start Color"]
		right_end_color = row["Right End Color"]
		right_glow = row["Right Glow"]

		sm.shape_change(left_shape,right_shape)
		sm.set_glow(left_glow, right_glow)
		sm.generate_gradients(left_start_color, right_start_color, left_end_color, right_end_color)
		

		framecount = 0
		while not event.getKeys(keyList=['q']):

			win.flip()
			framecount += 1

		rowcount += 1

	sys.exit()


def subjectCheck(subject):
	if re.search("^s\d*$", subject):
		return subject
	else:
		print "Invalid subject id! An id should be an 's' followed by only numbers."
		return subjectCheck(input("Please enter a valid subject id: "))

def activate_glow(shape, color, add_or_sub):

	return








if __name__ == "__main__":
    main()
