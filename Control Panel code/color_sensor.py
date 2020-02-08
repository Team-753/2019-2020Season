#!/usr/bin/env python3

import wpilib
from rev.color import ColorSensorV3

class ColorSensor(self):
	def __init__(self):
		self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
		self.predictedColor = ""
		self.rotations = 0
		self.lastColorIndex = 0
		self.colorOrder = ["yellow","red","green","cyan"]
	
	def predictColor(self):
		red = self.colorSensor.getColor().red
		green = self.colorSensor.getColor().green
		blue = self.colorSensor.getColor().blue
		
		if 0.29 < red < 0.53 and 0.33 < green < 0.46 and 0.13 < blue < 0.26:
			self.predictedColor = "red"
		elif 0.26 < red < 0.35 and 0.49 < green < 0.57 and 0.12 < blue < 0.24:
			self.predictedColor = "yellow"
		elif 0.16 < red < 0.25 and 0.48 < green < 0.58 and 0.24 < blue < 0.28:
			self.predictedColor = "green"
		elif 0.11 < red < 0.23 and 0.41 < green < 0.47 and 0.31 < blue < 0.47:
			self.predictedColor = "cyan"
		else:
			self.predictedColor = "???"
		
		return(self.predictedColor)
		
	def startRotationCount(self):
		
		if self.lastColorIndex <= 2:
			if self.predictedColor == self.colorOrder[self.lastColorIndex + 1]:
				self.rotations += 0.125
				self.lastColorIndex += 1
		elif self.lastColorIndex == 3:
			if self.predictedColor == self.colorOrder[self.lastColorIndex - 3]:
				self.rotations += 0.125
				self.lastColorIndex -= 3
		
	def checkRotationCount(self):
		
		return(self.rotations)
		
	def resetRotationCount(self):
		
		self.rotations = 0
		
if __name__ == "__main__":
	wpilib.run(colorSensor)