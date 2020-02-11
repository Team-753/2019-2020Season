import wpilib
import math
import rev

class Climb:
	def __init__(self):
		self.climbID = 9
		self.upButtonID = 1
		self.joystick = wpilib.Joystick #change this to the joystick on robot.py
		self.climbMotor = rev.CANSparkMax(climbID, MotorType.kBrushless)
		self.upButton = wpilib.SmartDashboard.getStickButton(self.joystick,self.upButtonID)