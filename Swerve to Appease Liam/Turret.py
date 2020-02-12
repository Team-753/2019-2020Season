import wpilib
import rev

class Turret: #this is currently just manual control, but motors can only be instantiated once so
	def __init__(self, rotateID, flyWheelID, speed): #eventually all the turret stuff will go here
		self.rotateMotor = rev.CANSparkMax(rotateID, MotorType.kBrushless)
		self.rotateEncoder = self.rotateMotor.getEncoder()
		self.flyWheelMotor = rev.CANSparkMax(flyWheelID, MotorType.kBrushless)
		self.speed = speed
	def rotate(self):
		if self.rotateEncoder < threshold:
			pass