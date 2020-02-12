import wpilib
import rev

class Feeder:
	def __init__(self): #feederMotor ID and speed of the motor
		self.feederMotor = rev.CANSparkMax(10, MotorType.kBrushless)
		self.speed = 1
	def feed(self):
		self.feederMotor.set(self.speed)
	def puke(self):
		self.feederMotor.set(-self.speed)
	def coast(self):
		self.feederMotor.setIdleMode(rev.IdleMode.kCoast)
	def brake(self):
		self.feederMotor.setIdleMode(rev.IdleMode.kBrake)