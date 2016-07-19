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

	#parameters: Anumber Arate Atime Acolor Aglow Bnumber Brate Btime Bcolor Bglow Ashape Bshape
	#response: Anumber Arate Atime Acolor Aglow Bnumber Brate Btime Bcolor Bglow Ashape Bshape


	parameters = []
	for row in parametersreader:
	 	parameters.append(row)

	random.shuffle(parameters)
	rowcount = 2
	sm = shape_Manager(win, sqsize, pos1, pos2, background_color)

	for row in parameters:
		Ashape = row["A Shape"]
		Acolor = row["A Color"]
		Aglow = row["A Glow"]

		Bshape = row["B Shape"]
		Bcolor = row["B Color"]
		Bglow = row["B Glow"]

		sm.shape_change(Ashape, Bshape)

		gradient = linear_gradient("#FF5733", "#ff876e")
		##9E3923
		# gr_red = gradient['r']
		# gr_blue = gradient['b']
		# gr_green = gradient['g']
		# for c in range(0,10):
		# 	circle1.fillColor = [gr_red[c], gr_green[c], gr_blue[c]]
		# 	win.flip()
		# 	time.sleep(2)
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
