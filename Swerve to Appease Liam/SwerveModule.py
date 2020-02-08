import math
import rev
import hal
from networktables import NetworkTables

class SwerveModule:
	wheelDiameter = 4 #inches
	turnMotorEncoderConversion = 20 #NEO encoder gives 0-18 as 1 full rotation
	absoluteEncoderConversion = .08877
	
	kP = .0039
	kI = 0
	kD = 0
	
	def __init__(self,driveID,turnID,encoderID,encoderOffset):
		self.driveMotor = rev.CANSparkMax(driveID,rev.MotorType.kBrushless)
		self.turnMotor = rev.CANSparkMax(turnID,rev.MotorType.kBrushless)
		self.turnEncoder = self.turnMotor.getEncoder()
		self.turnEncoder.setPositionConversionFactor(turnMotorEncoderConversion) #now is 0-360
		
		self.absoluteEncoder = wpilib.AnalogInput(encoderID)
		self.absolutePosition = self.absoluteEncoder.getValue()*absoluteEncoderConversion
		
		self.offset = encoderOffset
		
	def encoderBoundedPosition(self):
		position = self.turnEncoder.getPosition()%360 #this limits the encoder input
		if position < 0: #to be on a single circle
			position += 360
		if position < 90: #this translates those values to correspond with what the
			position += 90 #atan2 function returns (-180, 180)
		else:
			position -= 270
		return position
		
	def move(self,speed,angle):
		
		
	def zeroEncoder(self):
		self.turnEncoder.setPosition(self.absolutePosition - self.offset)
		
	def brake(self):
		self.driveMotor.setIdleMode(rev.IdleMode.kBrake)
		self.turnMotor.setIdleMode(rev.IdleMode.kBrake)
		
	def coast(self):
		self.driveMotor.setIdleMode(rev.IdleMode.kCoast)
		self.turnMotor.setIdleMode(rev.IdleMode.kCoast)
		