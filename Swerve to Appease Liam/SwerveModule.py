
import wpilib
import math
import rev
from wpilib import controller as controller


class SwerveModule():
	def __init__(self):
		pass
		
	def Module(driveID,turnID,absEncoderID,encoderOffset,encoderConversion,speed,angle):
		kP = .0039
		kI = 0
		kD = 2.0e-6
		PIDTolerance = 1.0
		
		target = 0
		
		turnTolerance = .1
		driveTolerance = .1
	
		driveMotor = rev.CANSparkMax(driveID, rev.MotorType.kBrushless)
		turnMotor = rev.CANSparkMax(turnID, rev.MotorType.kBrushless)
		turnEncoder = wpilib.AnalogInput(absEncoderID)
		
		positionTarget = angle
		revTarget = speed
		
		turnController = wpilib.controller.PIDController(kP, kI, kD)
		#self.driveController = wpilib.controller.PIDController(self.kP, self.kI, self.kD)
		
		turnController.setTolerance(turnTolerance)
		#self.driveController.setTolerance(self.driveTolerance)
		
		turnController.enableContinuousInput(-180, 180)
		#self.driveController.enableContinuousInput(-1,1) 
		
		turnController.setSetpoint(positionTarget)
		#self.driveController.setSetpoint(self.revTarget)
		#I do not know whether we will be doing velocity for drive control
		turnMotor.set(turnController.calculate(encoderConversion*turnEncoder.getValue()+encoderOffset-180))
		driveMotor.set(revTarget)
		
	
