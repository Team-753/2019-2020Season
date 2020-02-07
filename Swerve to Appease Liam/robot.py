#!/usr/bin/env python3

import wpilib
import math
import rev
from wpilib import controller as controller
import DriveTrain

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		self.joystick = wpilib.Joystick(0)
		self.joystickDeadband = .15
	
	def checkDeadband(self, axis):
		if abs(axis) < self.joystickDeadband:
			axis = 0
		return axis
	def autonomousInit(self):
		pass
	def autonomousPeriodic(self):
		pass
	def teleopInit(self):
		print('teleop started')
		
		#self.brakeMode()
	def teleopPeriodic(self):
		print(DriveTrain.Drive.getEncoders())
		
		x = self.checkDeadband(self.joystick.getX())
		y = self.checkDeadband(self.joystick.getY())
		z = self.checkDeadband(self.joystick.getZ())
		DriveTrain.Drive.Move(x,y,z)
		
		
		
	def disabledInit(self):
		pass

if __name__ == "__main__":
	wpilib.run(MyRobot)
