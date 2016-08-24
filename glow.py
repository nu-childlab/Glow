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
	scrwidth = 1280
	scrheight = 720
	#the length of the square's sides; the other shapes are calculated to fit within the square.
	#the length of the square = the diameter of the circle = the base and height of the triangle.
	sqsize = scrwidth/5
	#The positions are from the center of the screen, and mirror each other.
	pos1 = -scrwidth/5
	pos2 = -pos1
	background_color = [175,175,175]

	win = visual.Window([scrwidth,scrheight], units='pix', monitor='testMonitor', color=[175,175,175], colorSpace="rgb255")

	framerate = win.getActualFrameRate()
	seconds_per_frame = 1/framerate

	# #ifi = .0169
	# ifi = 1/framerate

	# read parameters file and open response file below
	parametersfile = open('glowparameters.csv', 'rU')
	parametersreader = csv.DictReader(parametersfile)
	# responsefile = open('glowresponses.csv', 'wb')
	# responsefields = ['Response', 'RT']
	# responsewriter = csv.DictWriter(responsefile, responsefields)
	# responsewriter.writeheader()

	#create a timer
	timer = core.Clock()

	parameters = []
	with open('glowparameters.csv', 'rU') as f:
		parametersreader = csv.DictReader(f)
		for row in parametersreader:
		 	parameters.append(row)

	random.shuffle(parameters)
	sm = shape_Manager(win, sqsize, pos1, pos2, background_color)

	for row in parameters:
		left_shape = row["Left Shape"]
		left_start_color = row["Left Start Color"]
		left_end_color = row["Left End Color"]
		left_glow = int(row["Left Glow"])
		left_v1 = float(row["Left Variable 1"])
		left_v1_type = row["L1 value type"]
		left_v2 = float(row["Left Variable 2"])
		left_v2_type = row["L2 value type"]

		right_shape = row["Right Shape"]
		right_start_color = row["Right Start Color"]
		right_end_color = row["Right End Color"]
		right_glow = int(row["Right Glow"])
		right_v1 = float(row["Right Variable 1"])
		right_v1_type = row["R1 value type"]
		right_v2 = float(row["Right Variable 2"])
		right_v2_type = row["R2 value type"]

		row_number = row["Row Number"]

		sm.shape_change(left_shape,right_shape, row_number)
		sm.set_glow(left_glow, right_glow)
		runtime = sm.variable_calc(left_v1, left_v1_type, left_v2, left_v2_type, right_v1, right_v1_type, right_v2, right_v2_type, row_number, framerate)


		#sm.set_colors(left_start_color, right_start_color, left_end_color, right_end_color)
		sm.generate_gradients(left_start_color, right_start_color, left_end_color, right_end_color)


		framecount = 0
		# while not event.getKeys(keyList=['q']):
		#
		# 	win.flip()
		# 	framecount += 1
		temptime = max(sm.right_cycle_end, sm.left_cycle_end)
		for x in range(0,temptime):
			sm.animate_colors()
			win.flip()


	sys.exit()


def subjectCheck(subject):
	if re.search("^s\d*$", subject):
		return subject
	else:
		print "Invalid subject id! An id should be an 's' followed by only numbers."
		return subjectCheck(input("Please enter a valid subject id: "))



if __name__ == "__main__":
    main()
