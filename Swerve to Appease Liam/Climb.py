import wpilib
import rev

class Climb:
	def __init__(self): #climbMotor ID and speed of the motor
		self.climbMotor = rev.CANSparkMax(9, MotorType.kBrushless)
		self.speed = 1
	def extend(self):
		self.climbMotor.set(self.speed)
	def contract(self):
		self.climbMotor.set(-self.speed)
	def coast(self):
		self.climbMotor.setIdleMode(rev.IdleMode.kCoast)
	def brake(self):
		self.climbMotor.setIdleMode(rev.IdleMode.kBrake)