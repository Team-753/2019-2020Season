import wpilib
import rev

class Climb:
	def __init__(self, motorID, speed):
		self.climbMotor = rev.CANSparkMax(ID, MotorType.kBrushless)
		self.speed = speed
	def extend(self):
		self.climbMotor.set(self.speed)
	def contract(self):
		self.climbMotor.set(-self.speed)
	def coast(self):
		self.climbMotor.setIdleMode(rev.IdleMode.kCoast)
	def brake(self):
		self.climbMotor.setIdleMode(rev.IdleMode.kBrake)