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

def main(): 

	# subject = str(raw_input("Subject Number: "))
	# subject = subjectCheck(subject)
	# print subject

	#2560, 1440
	scrwidth = 1280
	scrheight = 720
	win = visual.Window([scrwidth,scrheight], units='pix', monitor='testMonitor', color=[175,175,175], colorSpace="rgb255")

	framerate = win.getActualFrameRate()

	# Measuring framerate
	# nIntervals = 100
	# progBar = visual.GratingStim(win, tex=None, mask=None,
	#     size=[0, 0.05], color='red', pos=[0, -0.9], autoLog=False)
	# myStim = visual.GratingStim(win, tex='sin', mask='gauss',
	#     size=300, sf=0.05, units='pix', autoLog=False)
	# win.recordFrameIntervals = True
	# for frameN in range(nIntervals + 1):
	#     progBar.setSize([2.0 * frameN/nIntervals, 0.05])
	#     progBar.draw()
	#     myStim.setPhase(0.1, '+')
	#     myStim.draw()
	#     if event.getKeys():
	#         print 'stopped early'
	#         break
	#     win.logOnFlip(msg='frame=%i' %frameN, level=logging.EXP)
	#     win.flip()
	# win.fullscr = False

	# # calculate some values
	# intervalsMS = pylab.array(win.frameIntervals) * 1000
	# ifi = pylab.mean(intervalsMS)
	# print ifi

	#The above calculations mean that the framerate is stored in ifi
	#If you'd like to skip it, just comment out that code and set ifi below
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
	#vertices=[[0,0],[25,-50],[-25,-50]]

	#the length of the square's sides; the other shapes are calculated to fit within the square.
	#the length of the square = the diameter of the circle = the base and height of the triangle.
	sqsize = scrwidth/5
	#The positions are from the center of the screen, and mirror each other.
	pos1 = -scrwidth/5
	pos2 = -pos1

	triangle1 = visual.ShapeStim(win,size=[sqsize/2,sqsize], lineColor=[175,175,175],fillColor=[255,0,0], pos=[pos1,-sqsize/4], units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
	square1 = visual.Rect(win,lineColor=[175,175,175],fillColor=[0,255,0],size=[sqsize,sqsize],pos=[pos1,0],units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
	circle1 = visual.Circle(win, lineColor=[175,175,175], fillColor=[0,0,255], radius=sqsize/4, pos=[pos1,0], units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")

	triangle2 = visual.ShapeStim(win,size=[sqsize/2,sqsize], lineColor=[175,175,175],fillColor=[255,0,0], pos=[pos2,-sqsize/4], units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
	square2 = visual.Rect(win,lineColor=[175,175,175],fillColor=[0,255,0],size=[sqsize,sqsize],pos=[pos2,0],units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
	circle2 = visual.Circle(win, lineColor=[175,175,175], fillColor=[0,0,255], radius=sqsize/4, pos=[pos2,0], units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
	
	

	parameters = []
	for row in parametersreader:
		parameters.append(row)

	random.shuffle(parameters)
	rowcount = 2
	for row in parameters:
		Ashape = row["A Shape"]
		Acolor = row["A Color"]
		Aglow = row["A Glow"]
		Anumber = row["A Number"]
		Atime = row["A Time"]
		Arate = row["A Rate"]

		Bshape = row["B Shape"]
		Bcolor = row["B Color"]
		Bglow = row["B Glow"]
		Bnumber = row["B Number"]
		Btime = row["B Time"]
		Brate = row["B Rate"]

		if re.search("triangle", Ashape, re.IGNORECASE):
			triangle1.setAutoDraw(1)
			square1.setAutoDraw(0)
			circle1.setAutoDraw(0)
		elif re.search("square", Ashape, re.IGNORECASE):
			triangle1.setAutoDraw(0)
			square1.setAutoDraw(1)
			circle1.setAutoDraw(0)
		elif re.search("circle", Ashape, re.IGNORECASE):
			triangle1.setAutoDraw(0)
			square1.setAutoDraw(0)
			circle1.setAutoDraw(1)
		else:
			raise ValueError("Error in row " + str(rowcount) + ": A shape is unidentified. Ensure that the column's calue is square, triangle, or circle.")

		if re.search("triangle", Bshape, re.IGNORECASE):
			triangle2.setAutoDraw(1)
			square2.setAutoDraw(0)
			circle2.setAutoDraw(0)
		elif re.search("square", Bshape, re.IGNORECASE):
			triangle2.setAutoDraw(0)
			square2.setAutoDraw(1)
			circle2.setAutoDraw(0)
		elif re.search("circle", Bshape, re.IGNORECASE):
			triangle2.setAutoDraw(0)
			square2.setAutoDraw(0)
			circle2.setAutoDraw(1)
		else:
			raise ValueError("Error in row " + str(rowcount) + ": B shape is unidentified. Ensure that the column's calue is square, triangle, or circle.")

		while not event.getKeys(keyList=['q']):
			# triangle1.draw()  
			# square1.draw()  
			# circle1.draw()
			# triangle2.draw()  
			# square2.draw()  
			# circle2.draw()
			win.flip() 	

		rowcount += 1

	sys.exit()


def subjectCheck(subject):
	if re.search("^s\d*$", subject):
		return subject
	else:
		print "Invalid subject id! An id should be an 's' followed by only numbers."
		return subjectCheck(input("Please enter a valid subject id: "))









if __name__ == "__main__":
    main()

