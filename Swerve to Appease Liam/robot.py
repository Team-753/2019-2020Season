#!/usr/bin/env python3

import wpilib
import math
import rev
from wpilib import controller as controller
from DriveTrain import DriveTrain
from navx import AHRS

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		self.navx = AHRS.create_spi()
		self.navx.reset()
		
		self.joystick = wpilib.Joystick(0)
		self.joystickDeadband = .2
		
		self.drive = DriveTrain() #keep in mind that these are all arbitrary names
		self.drive.zeroEncoders() #feel free to change the weird ones
		self.fieldOriented = False
		
		self.scaling = .5
		wpilib.SmartDashboard.putNumber("Joystick scale factor", self.scaling)
		wpilib.SmartDashboard.putNumber("Joystick deadband", self.joystickDeadband)
		wpilib.SmartDashboard.putBoolean("Field Oriented", self.fieldOriented)
		
	def checkDeadband(self, axis):
		deadband = wpilib.SmartDashboard.getNumber("Joystick deadband", self.joystickDeadband)
		if abs(axis) < deadband:
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
		self.navx.reset() #please delete this before competition
		print('teleop started')
		
	def teleopPeriodic(self):
		scale = wpilib.SmartDashboard.getNumber("Joystick scale factor", self.scaling)
		fieldOriented = wpilib.SmartDashboard.getBoolean("Field Oriented", self.fieldOriented)
		
		x = scale*self.checkDeadband(self.joystick.getX())
		y = -scale*self.checkDeadband(self.joystick.getY())
		z = scale*self.checkDeadband(self.joystick.getZ())
		
		angle = -1*self.navx.getAngle() + 90
		wpilib.SmartDashboard.putNumber("angle",angle)
		angle *= math.pi/180
		
		if fieldOriented:
			cos = math.cos(angle)
			sin = math.sin(angle)
			temp = x*sin - y*cos
			y = x*cos + y*sin
			x = temp
		
		if max(abs(x),abs(y),abs(z)) != 0:
			self.drive.move(x,y,z)
		else:
			self.drive.stationary()
		
	def disabledInit(self):
		self.drive.coast()

if __name__ == "__main__":
	wpilib.run(MyRobot)