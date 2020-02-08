import math
import rev
import wpilib
from networktables import NetworkTables
from wpilib import controller as controller

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
		self.turnEncoder.setPositionConversionFactor(self.turnMotorEncoderConversion) #now is 0-360
		
		self.absoluteEncoder = wpilib.AnalogInput(encoderID)
		self.absolutePosition = self.absoluteEncoder.getValue()*self.absoluteEncoderConversion
		
		self.offset = encoderOffset
		
		self.turnController = wpilib.controller.PIDController(self.kP, self.kI, self.kD)
		self.turnController.enableContinuousInput(-180,180) #the angle range we decided to make standard
		
	def encoderBoundedPosition(self):
		position = self.turnEncoder.getPosition()%360 #this limits the encoder input
		if position < 0: #to be on a single circle
			position += 360
		if position < 90: #this translates those values to correspond with what the
			position += 90 #atan2 function returns (-180, 180)
		else:
			position -= 270
		return position
		
	def move(self,driveSpeed,angle):
		'''I finally remembered what the thing I kept forgetting about was. Once swerve is working well enough,
		we should add checks for better efficiency of moving. At a basic level, that could be making it so that
		in this method, there is logic so that rather than moving all the way, individual modules would move to
		the opposite side and just reverse the drive motors. More advanced control would be something in the
		DriveTrain class that uses the turn motors' collective positions, goals, and velocities to tell them which
		way they should turn. Could also have something in the module class that scales down drive speed as the module
		is turning. All of these are just ways to limit the effect of turning a module while attempting to drive,
		by either slowing down the driving or at least making the offset synchronized. I can explain more in-person'''
		
		position = self.encoderBoundedPosition()
		
		self.turnController.setSetpoint(angle) #tells the PID controller what our goal is
		turnSpeed = self.turnController.calculate(position) #gets the ideal speed from the PID controller
		
		self.driveMotor.set(driveSpeed)
		self.turnMotor.set(turnSpeed)
		
	def stationary(self):
		self.driveMotor.set(0)
		self.turnMotor.set(0)
		
	def zeroEncoder(self):
		self.turnEncoder.setPosition(self.absolutePosition - self.offset)
		
	def brake(self):
		self.driveMotor.setIdleMode(rev.IdleMode.kBrake)
		self.turnMotor.setIdleMode(rev.IdleMode.kBrake)
		
	def coast(self):
		self.driveMotor.setIdleMode(rev.IdleMode.kCoast)
		self.turnMotor.setIdleMode(rev.IdleMode.kCoast)
		