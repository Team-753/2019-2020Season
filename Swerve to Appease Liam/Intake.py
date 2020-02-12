import wpilib
import rev

class Intake:
	def __init__(self, motorID, speed):
		self.intakeMotor = rev.CANSparkMax(ID, MotorType.kBrushless)
		self.speed = speed
	def collect(self):
		self.intakeMotor.set(self.speed)
	def expel(self):
		self.intakeMotor.set(-self.speed)
	def coast(self):
		self.intakeMotor.setIdleMode(rev.IdleMode.kCoast)
	def brake(self):
		self.intakeMotor.setIdleMode(rev.IdleMode.kBrake)