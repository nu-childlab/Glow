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

class shape_Manager():
    """A class to manage the glowing shapes and their colors.
    There's a lot of class variables. Maybe I'll list them later."""
    def __init__(self, win, sqsize, pos1, pos2, background_color):
        """Creates the shape stimuli. They'll be modified instead of recreated
        each time in order to save time.
        This ONLY happens once per run of the experiment."""
        self.left_triangle = visual.ShapeStim(win,size=[sqsize/2,sqsize], lineColor=background_color,fillColor=[255,0,0],
            pos=[pos1,-sqsize/4], units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
        self.left_square = visual.Rect(win,lineColor=background_color,fillColor=[0,255,0],size=[sqsize,sqsize],
            pos=[pos1,0],units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
        self.left_circle = visual.Circle(win, lineColor=background_color, fillColor=[0,0,255], radius=sqsize/4,
            pos=[pos1,0], units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")

        self.right_triangle = visual.ShapeStim(win,size=[sqsize/2,sqsize], lineColor=background_color,fillColor=[255,0,0],
            pos=[pos2,-sqsize/4], units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
        self.right_square = visual.Rect(win,lineColor=background_color,fillColor=[0,255,0],size=[sqsize,sqsize],
            pos=[pos2,0],units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
        self.right_circle = visual.Circle(win, lineColor=background_color, fillColor=[0,0,255], radius=sqsize/4,
            pos=[pos2,0], units="pix", fillColorSpace="rgb255",lineColorSpace="rgb255")
        return

    def shape_change(self, left_shape, right_shape, rowcount):
        """Changes the active left and right shapes for the trial.
        These are the shapes that will be automatically drawn."""
        if re.search("triangle", left_shape, re.IGNORECASE):
            self.left_triangle.setAutoDraw(1)
            self.left_square.setAutoDraw(0)
            self.left_circle.setAutoDraw(0)
            self.left_active_shape = self.left_triangle
        elif re.search("square", left_shape, re.IGNORECASE):
            self.left_triangle.setAutoDraw(0)
            self.left_square.setAutoDraw(1)
            self.left_circle.setAutoDraw(0)
            self.left_active_shape = self.left_square
        elif re.search("circle", left_shape, re.IGNORECASE):
            self.left_triangle.setAutoDraw(0)
            self.left_square.setAutoDraw(0)
            self.left_circle.setAutoDraw(1)
            self.left_active_shape = self.left_circle
        else:
            raise ValueError("Error in row " + str(rowcount) + ": A shape is unidentified. Ensure that the column's value is square, triangle, or circle.")

        if re.search("triangle", right_shape, re.IGNORECASE):
            self.right_triangle.setAutoDraw(1)
            self.right_square.setAutoDraw(0)
            self.right_circle.setAutoDraw(0)
            self.right_active_shape = self.right_triangle
        elif re.search("square", right_shape, re.IGNORECASE):
            self.right_triangle.setAutoDraw(0)
            self.right_square.setAutoDraw(1)
            self.right_circle.setAutoDraw(0)
            self.right_active_shape = self.right_square
        elif re.search("circle", right_shape, re.IGNORECASE):
            self.right_triangle.setAutoDraw(0)
            self.right_square.setAutoDraw(0)
            self.right_circle.setAutoDraw(1)
            self.right_active_shape = self.right_circle
        else:
            raise ValueError("Error in row " + str(rowcount) + ": B shape is unidentified. Ensure that the column's value is square, triangle, or circle.")


        self.left_frame_count = 0
        self.right_frame_count = 0
        return

    def variable_calc(self, left_v1, left_v1_type, left_v2, left_v2_type, right_v1, right_v1_type, right_v2, right_v2_type, rowcount, framerate):
        """Should turn the two variables from the parameters file into a set
        of 3 variables: total time of animation, rate of glowing/flashing (how
        many times it will complete a full cycle per second), and how many full
        cycles it will complete. The third variable will be calculated from the
        other two."""
        self.left_time = 0
        self.left_rate = 0
        self.left_number = 0
        self.right_time = 0
        self.right_rate = 0
        self.right_number = 0

        #LEFT VARIABLE 1
        if re.search("time", left_v1_type, re.IGNORECASE):
            self.left_time = left_v1
        elif re.search("number", left_v1_type, re.IGNORECASE):
            self.left_number = left_v1
        elif re.search("rate", left_v1_type, re.IGNORECASE):
            self.left_rate = left_v1
        else:
            raise ValueError("Error in row " + str(rowcount) + ": Left Variable 1 Type is unidentified. Ensure that the column's value is time, number, or rate.")

        #LEFT VARIABLE 2
        #var2 is time
        if re.search("time", left_v2_type, re.IGNORECASE):
            if self.left_time:
                raise ValueError("Error in row " + str(rowcount) + ": Left Variable 1 Type and Left Variable 2 Type are the same. Please ensure that they are two different values from: time, number, or rate.")
            elif self.left_rate:
                #time and rate are defined; number is calculated
                self.left_time = left_v2
                self.left_number = self.left_rate * self.left_time
            elif self.left_number:
                #time and number are defined; rate is calculated
                self.left_time = left_v2
                self.left_rate = self.left_number / self.left_time
            else:
                raise ValueError("Error in row " + str(rowcount) + ": Somehow, the first variable didn't get set! Make sure you're providing a valid variable type (time, rate, or number).")
        #var2 is number
        elif re.search("number", left_v2_type, re.IGNORECASE):
            if self.left_number:
                raise ValueError("Error in row " + str(rowcount) + ": Left Variable 1 Type and Left Variable 2 Type are the same. Please ensure that they are two different values from: time, number, or rate.")
            elif self.left_rate:
                #number and rate are defined; time is calculated
                self.left_number = left_v2
                self.left_time = self.left_number / self.left_rate
            elif self.left_time:
                #number and time are defined; rate is calculated
                self.left_number = left_v2
                self.left_rate = self.left_number / self.left_time
            else:
                raise ValueError("Error in row " + str(rowcount) + ": Somehow, the first variable didn't get set! Make sure you're providing a valid variable type (time, rate, or number).")
        #var2 is rate
        elif re.search("rate", left_v2_type, re.IGNORECASE):
            if self.left_rate:
                raise ValueError("Error in row " + str(rowcount) + ": Left Variable 1 Type and Left Variable 2 Type are the same. Please ensure that they are two different values from: time, number, or rate.")
            elif self.left_number:
                #rate and number are defined; time is calculated
                self.left_rate = left_v2
                self.left_time = self.left_number / self.left_rate
            elif self.left_time:
                #rate and time are defined; number is calculated
                self.left_rate = left_v2
                self.left_number = self.left_rate * self.left_time
            else:
                raise ValueError("Error in row " + str(rowcount) + ": Somehow, the first variable didn't get set! Make sure you're providing a valid variable type (time, rate, or number).")

        else:
            raise ValueError("Error in row " + str(rowcount) + ": Left Variable 2 Type is unidentified. Ensure that the column's value is time, number, or rate.")

        #RIGHT VARIABLE 1
        if re.search("time", right_v1_type, re.IGNORECASE):
            self.right_time = right_v1
        elif re.search("number", right_v1_type, re.IGNORECASE):
            self.right_number = right_v1
        elif re.search("rate", right_v1_type, re.IGNORECASE):
            self.right_rate = right_v1
        else:
            raise ValueError("Error in row " + str(rowcount) + ": Right Variable 1 Type is unidentified. Ensure that the column's value is time, number, or rate.")

        #RIGHT VARIABLE 2
        #var2 is time
        if re.search("time", right_v2_type, re.IGNORECASE):
            if self.right_time:
                raise ValueError("Error in row " + str(rowcount) + ": Right Variable 1 Type and Right Variable 2 Type are the same. Please ensure that they are two different values from: time, number, or rate.")
            elif self.right_rate:
                #time and rate are defined; number is calculated
                self.right_time = right_v2
                self.right_number = self.right_rate * self.right_time
            elif self.right_number:
                #time and number are defined; rate is calculated
                self.right_time = right_v2
                self.right_rate = self.right_number / self.right_time
            else:
                raise ValueError("Error in row " + str(rowcount) + ": Somehow, the first variable didn't get set! Make sure you're providing a valid variable type (time, rate, or number).")
        #var2 is number
        elif re.search("number", right_v2_type, re.IGNORECASE):
            if self.right_number:
                raise ValueError("Error in row " + str(rowcount) + ": Right Variable 1 Type and Right Variable 2 Type are the same. Please ensure that they are two different values from: time, number, or rate.")
            elif self.right_rate:
                #number and rate are defined; time is calculated
                self.right_number = right_v2
                self.right_time = self.right_number / self.right_rate
            elif self.right_time:
                #number and time are defined; rate is calculated
                self.right_number = right_v2
                self.right_rate = self.right_number / self.right_time
            else:
                raise ValueError("Error in row " + str(rowcount) + ": Somehow, the first variable didn't get set! Make sure you're providing a valid variable type (time, rate, or number).")
        #var2 is rate
        elif re.search("rate", right_v2_type, re.IGNORECASE):
            if self.right_rate:
                raise ValueError("Error in row " + str(rowcount) + ": Right Variable 1 Type and Right Variable 2 Type are the same. Please ensure that they are two different values from: time, number, or rate.")
            elif self.right_number:
                #rate and number are defined; time is calculated
                self.right_rate = right_v2
                self.right_time = self.right_number / self.right_rate
            elif self.right_time:
                #rate and time are defined; number is calculated
                self.right_rate = right_v2
                self.right_number = self.right_rate * self.right_time
            else:
                raise ValueError("Error in row " + str(rowcount) + ": Somehow, the first variable didn't get set! Make sure you're providing a valid variable type (time, rate, or number).")

        else:
            raise ValueError("Error in row " + str(rowcount) + ": Right Variable 2 Type is unidentified. Ensure that the column's value is time, number, or rate.")

        # if self.left_time > self.right_time:
		# 	runtime = self.left_time
        # else:
		# 	runtime = self.right_time

        runtime = max(self.left_time, self.right_time)

        temptotalframes = round(runtime * framerate)
        #The total number of frames in the process for these shapes.
        self.left_totalframes = int(round(self.left_time*framerate))
        self.right_totalframes = int(round(self.right_time*framerate))

        #The number of frames in one cycle (starting and ending at the same color) of a glow or flash.
        #The weird half-and-full cycle calculations are because I want to make sure they all match up with rounding,
        #since they're used for interating through for loops and maintaining the timing.
        self.left_halfcycleframes = int(round((self.left_totalframes/self.left_number)/2))
        self.right_halfcycleframes = int(round((self.right_totalframes/self.right_number)/2))
        self.left_cycleframes = self.left_halfcycleframes*2
        self.right_cycleframes = self.right_halfcycleframes*2

        return runtime

    def set_glow(self,left_glow, right_glow):
        """Sets the glow values for the trial. 1 means it will glow through a
        range of colors. 0 means it will flash between full opacity and no
        opacity."""
        if left_glow:
            self.left_glow = 1
        else:
            self.left_glow = 0
        if right_glow:
            self.right_glow = 1
        else:
            self.right_glow = 0
        return

    def generate_gradients(self,left_start_color, right_start_color, left_end_color, right_end_color):
        """Generates color gradients for the left and right shapes.
        The gradient variables become lists of lists, where each inner list
        is an rgb tuple."""
        self.left_start_color = hex_to_RGB(left_start_color)
        self.right_start_color = hex_to_RGB(right_start_color)
        self.left_end_color = hex_to_RGB(left_end_color)
        self.right_end_color = hex_to_RGB(right_end_color)
        self.left_active_shape.fillColor = hex_to_RGB(left_start_color)
        self.right_active_shape.fillColor = hex_to_RGB(right_start_color)

        if self.left_glow:
            self.left_gradient = []
            gr = linear_gradient(left_start_color, left_end_color, self.left_halfcycleframes)
            for i in range(0, len(gr['r'])):
                self.left_gradient.append([gr['r'][i], gr['g'][i], gr['b'][i]])
            #Add the inverse gradient so it returns to the original color
            self.left_gradient = self.left_gradient + self.left_gradient[::-1]
        else:
            self.left_gradient = left_start_color
        if self.right_glow:
            self.right_gradient = []
            gr = linear_gradient(right_start_color, right_end_color, self.right_halfcycleframes)
            for i in range(0, len(gr['r'])):
                self.right_gradient.append([gr['r'][i], gr['g'][i], gr['b'][i]])
            self.right_gradient = self.right_gradient + self.right_gradient[::-1]
        else:
            self.right_gradient = right_start_color
        return

    def shape_glow(self, shape, gradient, framecount):
        """Helper function for animate_colors.
        Will advance the glowing shapes color by applying the next color
        in the gradient list."""
        shape.setFillColor(gradient[framecount])
        return

    def shape_flash(self, shape, color, framecount, endcycle):
        """Helper function for animate_colors.
        Will toggle the opacity at the appropriate time in the cycle."""
        if framecount < round(endcycle/2):
            shape.setOpacity(1)
        else:
            shape.setOpacity(0)
        return

    def animate_colors(self, count):
        """Makes one step/frame in the color-changing animation.
        It increments the shapes and changes their color according to the
        gradient or whether it should be flashing or not."""
        #If it's not done with the whole animation
        if count<self.left_totalframes:
            #Either glow or flash the shape
            if self.left_glow:
                self.shape_glow(self.left_active_shape, self.left_gradient, self.left_frame_count)
            else:
                self.shape_flash(self.left_active_shape, self.left_gradient, self.left_frame_count, self.left_cycleframes)
        if count<self.right_totalframes:
            if self.right_glow:
                self.shape_glow(self.right_active_shape, self.right_gradient, self.right_frame_count)
            else:
                self.shape_flash(self.right_active_shape, self.right_gradient, self.right_frame_count, self.right_cycleframes)

        self.left_frame_count += 1
        self.right_frame_count += 1
        if self.left_frame_count >= self.left_cycleframes:
            self.left_frame_count = 0
        if self.right_frame_count >= self.right_cycleframes:
            self.right_frame_count = 0

    def shape_clear(self):
        """Makes the active shapes stop being drawn"""
        self.left_active_shape.setAutoDraw(0)
        self.right_active_shape.setAutoDraw(0)
