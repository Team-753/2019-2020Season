import wpilib
import rev

class Climb:
	encoderConversionFactor = 64 #this isn't real and needs to be changed
	def __init__(self, motorID, speed):
		self.climbMotor = rev.CANSparkMax(ID, rev.MotorType.kBrushless)
		self.speed = speed
		self.climbEncoder = self.climbMotor.getEncoder()
		self.climbEncoder.setPositionConversionFactor(self.encoderConversionFactor)
	def extend(self):
		self.climbMotor.set(self.speed)
	def contract(self):
		self.climbMotor.set(-self.speed)
	def coast(self):
		self.climbMotor.setIdleMode(rev.IdleMode.kCoast)
	def brake(self):
		self.climbMotor.setIdleMode(rev.IdleMode.kBrake)
	def checkEncoder(self):
		position = self.climbEncoder.getPosition()
		return position
	def zeroEncoder(self):
		self.climbEncoder.setPosition(0)