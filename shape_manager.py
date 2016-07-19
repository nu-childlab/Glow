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

    def __init__(self, win, sqsize, pos1, pos2, background_color):
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

    def shape_change(self, left_shape, right_shape):
        if re.search("triangle", left_shape, re.IGNORECASE):
            self.left_triangle.setAutoDraw(1)
            self.left_square.setAutoDraw(0)
            self.left_circle.setAutoDraw(0)
        elif re.search("square", left_shape, re.IGNORECASE):
            self.left_triangle.setAutoDraw(0)
            self.left_square.setAutoDraw(1)
            self.left_circle.setAutoDraw(0)
        elif re.search("circle", left_shape, re.IGNORECASE):
            self.left_triangle.setAutoDraw(0)
            self.left_square.setAutoDraw(0)
            self.left_circle.setAutoDraw(1)
        else:
            raise ValueError("Error in row " + str(rowcount) + ": A shape is unidentified. Ensure that the column's value is square, triangle, or circle.")

        if re.search("triangle", right_shape, re.IGNORECASE):
            self.right_triangle.setAutoDraw(1)
            self.right_square.setAutoDraw(0)
            self.right_circle.setAutoDraw(0)
        elif re.search("square", right_shape, re.IGNORECASE):
            self.right_triangle.setAutoDraw(0)
            self.right_square.setAutoDraw(1)
            self.right_circle.setAutoDraw(0)
        elif re.search("circle", right_shape, re.IGNORECASE):
            self.right_triangle.setAutoDraw(0)
            self.right_square.setAutoDraw(0)
            self.right_circle.setAutoDraw(1)
        else:
            raise ValueError("Error in row " + str(rowcount) + ": B shape is unidentified. Ensure that the column's value is square, triangle, or circle.")

        def set_glow(left_glow, right_glow):
            self.left_glow = 1
            self.right_glow = 0

        def generate_gradients(left_start_color, right_start_color):
            if self.left_glow:
                self.left_gradient = []
            else:
                self.left_gradient = [left_color]
            if self.right_glow:
                self.right_gradient = []
            else:
                self.right_gradient[right_color]
