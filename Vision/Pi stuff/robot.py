import wpilib, ctre, math, logging
from wpilib.drive import MecanumDrive
from networktables import NetworkTables
from wpilib import CameraServer
import numpy
import math
from enum import Enum
import logging
import sys
import time
import threading

cond = threading.Condition()
notified = False

def connectionListener(connected, info):
	print(info, '; Connected=%s' % connected)
	with cond:
		notified = True 
		cond.notify()

# To see messages from networktables, you must setup logging 
NetworkTables.initialize() 
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
sd = NetworkTables.getTable('SmartDashboard') 

Yaw=sd.getValue('yaw', 0)


logging.basicConfig(level=logging.DEBUG)

class MyRobot(wpilib.TimedRobot):
	
	def robotInit(self):
		self.id =8
		
		
	def autonomousInit(self):
		pass
	def autonomousPeriodic(self):
		pass
	



		
	def teleopInit(self):
		pass
	def teleopPeriodic(self):
		#use this to control the motor: rev.CANSparkMax(4,rev.MotorType.kBrushless).set(0.5)
		print(Yaw)
		
if __name__ == '__main__':
	wpilib.run(MyRobot)