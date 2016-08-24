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
from color_functions import *
from shape_manager import shape_Manager
from python_experiment_functions import *

def main():
	#Get subject number
	subject = getSubjectId()

	# read parameters file and open response file below
	responsefile = open(subject + '_glowresponses.csv', 'ab')
	responsefields = ['Subject', 'Left Shape', 'Left Start Color', 'Left End Color', 'Left Glow',
		'Left Time', 'Left Rate', 'Left Number', 'Right Shape',
		'Right Start Color', 'Right End Color', 'Right Glow', 'Right Time',
		'Right Rate', 'Right Number', 'Color','Response', 'RT']
	responsewriter = csv.DictWriter(responsefile, responsefields)
	responsewriter.writeheader()

	parameters = []
	with open('glowparameters.csv', 'rU') as f:
		parametersreader = csv.DictReader(f)
		for row in parametersreader:
		 	parameters.append(row)

	random.shuffle(parameters)
	fullscreen = True
	background_color = [175,175,175]
	win, scrwidth, scrheight = window_creation(fullscreen, background_color)

	#the length of the square's sides; the other shapes are calculated to fit within the square.
	#the length of the square = the diameter of the circle = the base and height of the triangle.
	sqsize = scrwidth/5
	#The positions are from the center of the screen, and mirror each other.
	pos1 = -scrwidth/5
	pos2 = -pos1
	instructions_text = "In this experiment, you will be asked to evaluate sentences relative to short animations. For each animation, you will indicate whether the sentence accurately describes that animation by pressing 'f' for YES or 'j' for NO. You will be reminded of these response keys throughout."

	instructions_screen(win, scrwidth, scrheight, instructions_text)

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

		color = row["Color"]

		row_number = row["Row Number"]
		framerate = win.getActualFrameRate()
		seconds_per_frame = 1/framerate

		sm.shape_change(left_shape,right_shape, row_number)
		sm.set_glow(left_glow, right_glow)
		runtime = sm.variable_calc(left_v1, left_v1_type, left_v2, left_v2_type, right_v1, right_v1_type, right_v2, right_v2_type, row_number, framerate)

		sm.generate_gradients(left_start_color, right_start_color, left_end_color, right_end_color)


		framecount = 0

		temptime = max(sm.right_totalframes, sm.left_totalframes)
		for x in range(0,temptime):
			sm.animate_colors(x)
			win.flip()
		sm.shape_clear()
		r = response_screen(win, scrwidth, scrheight, 'The '+left_shape+' is more '+color+' than the '+right_shape+' is.', 'Press f for yes and j for no', ['f','j'])
		responsewriter.writerow({'Subject':subject,'Left Shape':left_shape, 'Left Start Color':left_start_color, 'Left End Color':left_end_color, 'Left Glow':left_glow,
			'Left Time':sm.left_time, 'Left Rate':sm.left_rate, 'Left Number':sm.left_number, 'Right Shape':right_shape,
			'Right Start Color':right_start_color, 'Right End Color':right_end_color, 'Right Glow':right_glow, 'Right Time':sm.right_time,
			'Right Rate':sm.right_rate, 'Right Number':sm.right_number, 'Color':color,'Response':r[0], 'RT':r[1]})

	responsefile.close()
	finish_screen(win, scrwidth, scrheight)
	sys.exit()



if __name__ == "__main__":
    main()
