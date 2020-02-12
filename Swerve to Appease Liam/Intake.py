import wpilib
import rev

class Feeder:
	def __init__(self): #intakeMotor ID and speed of the motor
		self.intakeMotor = rev.CANSparkMax(11, MotorType.kBrushless)
		self.speed = 1
	def collect(self):
		self.intakeMotor.set(self.speed)
	def expel(self):
		self.intakeMotor.set(-self.speed)
	def coast(self):
		self.intakeMotor.setIdleMode(rev.IdleMode.kCoast)
	def brake(self):
		self.intakeMotor.setIdleMode(rev.IdleMode.kBrake)