#!/usr/bin/env python3

import wpilib
import math
import rev
from wpilib import controller as controller
import DriveTrain.DriveTrain as DriveTrain

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		self.joystick = wpilib.Joystick(0)
		self.joystickDeadband = .15
		
		DriveTrain.zeroEncoders()
	def checkDeadband(self, axis):
		if abs(axis) < self.joystickDeadband:
			axis = 0
		return axis
	def autonomousInit(self):
		DriveTrain.brake()
		print('autonomous started')
	def autonomousPeriodic(self):
		pass
	def teleopInit(self):
		DriveTrain.zeroEncoders()
		DriveTrain.brake()
		print('teleop started')
		#self.brakeMode()
	def teleopPeriodic(self):
		x = self.checkDeadband(self.joystick.getX())
		y = self.checkDeadband(self.joystick.getY())
		z = self.checkDeadband(self.joystick.getZ())
		
		DriveTrain.drive(x,y,z)
		
	def disabledInit(self):
		DriveTrain.coast()

if __name__ == "__main__":
	wpilib.run(MyRobot)