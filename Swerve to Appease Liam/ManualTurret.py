import wpilib
import rev

class ManualTurret:
	def __init__(self, rotateID, flyWheelID, speed):
		self.rotateMotor = rev.CANSparkMax(rotateID, MotorType.kBrushless)
		self.rotateEncoder = self.rotateMotor.getEncoder()
		self.flyWheelMotor = rev.CANSparkMax(flyWheelID, MotorType.kBrushless)
		self.speed = speed
	def rotate(self):
		if self.rotateEncoder < threshold:
			pass