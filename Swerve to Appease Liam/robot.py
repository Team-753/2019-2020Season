#!/usr/bin/env python3

import wpilib
import math
import rev
from wpilib import controller as controller
from DriveTrain import DriveTrain

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		self.joystick = wpilib.Joystick(0)
		self.joystickDeadband = .15
		
		self.drive = DriveTrain() #keep in mind that these are all arbitrary names
		self.drive.zeroEncoders() #feel free to change the weird ones
	def checkDeadband(self, axis):
		if abs(axis) < self.joystickDeadband:
			axis = 0
		return axis
	def autonomousInit(self):
		self.drive.zeroEncoders()
		self.drive.brake()
		print('autonomous started')
	def autonomousPeriodic(self):
		pass
	def teleopInit(self):
		self.drive.zeroEncoders()
		self.drive.brake()
		print('teleop started')
		#self.brakeMode()
	def teleopPeriodic(self):
		x = self.checkDeadband(self.joystick.getX())
		y = self.checkDeadband(self.joystick.getY())
		z = self.checkDeadband(self.joystick.getZ())
		
		if max(abs(x),abs(y),abs(z)) != 0:
			self.drive.move(x,y,z)
		else:
			self.drive.stationary()
		
	def disabledInit(self):
		self.drive.coast()

if __name__ == "__main__":
	wpilib.run(MyRobot)