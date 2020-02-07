#!/usr/bin/env python3

import rev
import wpilib
import math

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		self.turnEncoder = wpilib.AnalogInput(0)
	def autonomousInit(self):
		pass
	def autonomousPeriodic(self):
		pass
	def teleopInit(self):
		pass
	def teleopPeriodic(self):
		# Read data from SmartDashboard
		oijhaeof = self.turnEncoder.getValue()*.08877
		print(str(oijhaeof))

if __name__ == "__main__":
	wpilib.run(MyRobot)