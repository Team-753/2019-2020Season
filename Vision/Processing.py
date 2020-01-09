#!/usr/bin/python3

"""
Sample program that uses a generated GRIP pipeline to detect red areas in an image and publish them to NetworkTables.
"""
import math
import cv2
import urllib
import networktables
import numpy
from networktables import NetworkTables
from S_proc import GripPipeline
import datetime
from time import sleep
from wpilib import CameraServer
import logging
import sys
import time
import threading

logging.basicConfig(level=logging.DEBUG)
sd = NetworkTables.getTable("SmartDashboard")
NetworkTables.initialize( server = '10.7.53.2') 
Pr_ang = 0

def Z_compute(rectangle):
	x, y, w, h = rectangle
	center_X = x + 0.5 * w 
	diff = 640 - center_X
	return(diff / 540)



def Rect_Math(rectangle):
	Orig_D = 8 #inches (original distance)
	Tru_H = 180 #pixel height of rectangle (original)
	True_W = 144
	
	x, y, w, h = rectangle
	distP = (Tru_H * Orig_D / h)
	print(str(rectangle))
	scaled_W = (h / Tru_H) * True_W
	adj_ang = math.degrees(numpy.arccos(w / scaled_W))
	
	
	return(adj_ang, distP)

def extra_processing(pipeline):
	global Pr_ang
	"""
	Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
	:param pipeline: the pipeline that just processed an image
	:return: None
	"""
	C_List = pipeline.filter_contours_output
	rectangle_List = []
	ang = 0
	dist = 0
	speedfactor = 1
	Z_Invert = 1
	Z_change = 0
	# Find the bounding boxes of the contours to get x, y, width, and height
	for contour in C_List:
		rectangle = cv2.boundingRect(contour)
		rectangle_List.insert(0, rectangle)

		
		 # we will usually have 2 contours
	if len(rectangle_List) == 2:
		print('here?')
		if rectangle_List[0][0] < rectangle_List[1][0]: #this distinguishes between left and right
			ang, dist = Rect_Math(rectangle_List[0])
			Z_change = Z_compute(rectangle_List[0]) 
		else:
			ang, dist = Rect_Math(rectangle_List[1])
			Z_change = Z_compute(rectangle_List[1])
	if len(rectangle_List) == 1: #only one was identified 
		ang, dist = Rect_Math(rectangle_List[0])
		Z_change = Z_compute(rectangle_List[0])
		
	if dist > 0 and numpy.isnan(ang) == False:
		
		
		
		if Pr_ang < ang:
			Z_Invert = -1
		if  Pr_ang > ang:
			Z_Invert = 1
			
		Pr_ang = ang
		
		X_adjust = dist * math.degrees(numpy.cos(ang))
		Y_adjust = dist * math.degrees(numpy.sin(ang))
		print(Z_change)

		# Publish to the '/vision' network table
		sd.putValue("adjust_x", X_adjust)
		sd.putValue("adjust_y", Y_adjust)
		sd.putValue("adjust_z", Z_Value)
		print('dist ' + str(dist) + '     ang  ' + str(ang) )
	
	

def main():
	
	print('Initializing NetworkTables')
	NetworkTables.initialize()

	print('Creating video capture')
	cap = cv2.VideoCapture(0)

	print('Creating pipeline')
	pipeline = GripPipeline()

	print('Running pipeline')
	while cap.isOpened():
		have_frame, frame = cap.read()
		if have_frame:
			pipeline.process(frame)
			extra_processing(pipeline)

	print('Capture closed')



if __name__ == '__main__':
	main()