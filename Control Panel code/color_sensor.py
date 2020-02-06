#!/usr/bin/env python3

import wpilib
from rev.color import ColorSensorV3

class ColorSensor(self):
	def __init__(self):
		colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
		predictedColor = ""
		rotations = 0
		lastColorIndex = 0
		colorOrder = ["yellow","red","green","cyan"]
	
	def predictColor(self):
		red = colorSensor.getColor().red
		green = colorSensor.getColor().green
		blue = colorSensor.getColor().blue
		
		if 0.29 < red < 0.53 and 0.33 < green < 0.46 and 0.13 < blue < 0.26:
			predictedColor = "red"
		elif 0.26 < red < 0.35 and 0.49 < green < 0.57 and 0.12 < blue < 0.24:
			predictedColor = "yellow"
		elif 0.16 < red < 0.25 and 0.48 < green < 0.58 and 0.24 < blue < 0.28:
			predictedColor = "green"
		elif 0.11 < red < 0.23 and 0.41 < green < 0.47 and 0.31 < blue < 0.47:
			predictedColor = "cyan"
		else:
			predictedColor = "???"
		
		return(predictedColor)
		
	def startRotationCount(self):
		
		if lastColorIndex <= 2:
			if predictedColor == colorOrder[lastColorIndex + 1]:
				rotations += 0.125
				lastColorIndex += 1
		elif lastColorIndex == 3:
			if predictedColor == colorOrder[lastColorIndex - 3]:
				rotations += 0.125
				lastColorIndex -= 3
		
	def checkRotationCount(self):
		
		return(rotations)
		
	def resetRotationCount(self):
		
		rotations = 0
		
if __name__ == "__main__":
	wpilib.run(colorSensor)