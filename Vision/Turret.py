import wpilib
from wpilib import controller as controller
import math
import rev
from enum import Enum
import logging
import sys
import time
import threading
from networktables import NetworkTables

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
	 print(info, '; Connected=%s' % connected)
	 with cond:
		 notified[0] = True
		 cond.notify()

NetworkTables.initialize()
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
sd = NetworkTables.getTable('chameleon-vision').getSubTable('Live! Cam Chat HD VF0790')

class TurretAuto:
	def __init__(self):
		self.yaw = sd.getEntry('yaw').getDouble(0)
		self.pitch = sd.getEntry('pitch').getDouble(0)
		
		self.flywheelPort = 0
		#determine from Chazzy-poo
		self.hoodReduction = 12
		
		
		self.turretMotorID = 11
		self.spinMotorID = 12
		self.spinMotor2ID = 13
		
		self.turretMotor = rev.CANSparkMax(self.turretMotorID,rev.MotorType.kBrushless)
		self.spinMotor = rev.CANSparkMax(self.spinMotorID,rev.MotorType.kBrushless)
		self.spinMotor2 = rev.CANSparkMax(self.spinMotor2ID,rev.MotorType.kBrushless)
		
		self.kP = 0.0
		self.kI = 0.0
		self.kD = 0.0
		
		self.turretTurnController = wpilib.controller.PIDController(self.kP,self.kI,self.kD)
		self.turretTurnController.setSetpoint(0)
		self.turretTurnController.setBounds(0,360)
		self.turretTurnController.setTolerance(0.1)
		
		self.sP = 0.0
		self.sI = 0.0
		self.sD = 0.0
		self.cruisingVelocity = 5500 #in rpm
		self.minVelocity = 1000
		
		self.spinController = rev._impl.CANPIDController(self.spinMotor)
		self.spinController.setP(self.sP,self.flywheelPort)
		self.spinController.setI(self.sI,self.flywheelPort)
		self.spinController.setD(self.sD,self.flywheelPort)
		self.spinController.setSmartMotionMaxVelocity(self.cruisingVelocity,self.flywheelPort)
		self.spinController.setSmartMotionMinOutputVelocity(self.minVelocity, self.flywheelPort)
		
		self.spinController2 = rev._impl.CANPIDController(self.spinMotor2)
		self.spinController2.setP(self.sP,self.flywheelPort)
		self.spinController2.setI(self.sI,self.flywheelPort)
		self.spinController2.setD(self.sD,self.flywheelPort)
		self.spinController2.setSmartMotionMaxVelocity(self.cruisingVelocity,self.flywheelPort)
		self.spinController2.setSmartMotionMinOutputVelocity(self.minVelocity, self.flywheelPort)
		
		self.stallLimit = 78
		self.freeLimit  = 22
		self.limitRPM  = 2200
		self.spinMotor.setSmartCurrentLimit(self.stallLimit,self.freeLimit,self.limitRPM)
		
		
		self.hoodServo = wpilib.PWM(0)
		#not a definite value, just guesstimation
		self.defaultVelocity = 4500
		self.startAngle = 30 #need to determine physically what the angle is initially
		self.idealAngle = 35
	def velocityControl(self,desiredVelocity):
		
		self.spinController.setReference(desiredVelocity,rev.ControlType.kSmartVelocity,self.flywheelPort)
		self.spinController2.setReference(desiredVelocity,rev.ControlType.kSmartVelocity,self.flywheelPort)
		hoodAngle = 90-self.idealAngle+self.startAngle
		self.hoodServo.setPosition((90-self.idealAngle+self.startAngle)/360)
		
	def angularControl(self):
		
		
		
		
		self.spinController.setReference(self.defaultVelocity,rev.ControlType.kSmartVelocity,self.flywheelPort)
		self.spinController2.setReference(self.defaultVelocity,rev.ControlType.kSmartVelocity,self.flywheelPort)
		self.angTarget = 1#Liam math needed
		
		#the angle of the circular hood section
		self.turretAngle =90 + -self.angTarget + self.startAngle
		
		self.hoodServo.setPosition((self.hoodReduction*self.turretAngle)/360)
		
	def turretAlign(self):
		bop = self.yaw
		turretOutput = self.turretTurnController.calculate(bop)
		self.turretMotor.set(turretOutput)
	
	def turretShoot(self):
		#the turret must first align with the plane of the center of the target
		self.turretAlign()
		
		
		vDesired= #(insert Liam math here
		
		if (vDesired > self.maxVelocity) or (vDesired < self.minVelocity):
			#Angular control
			
			angularControl()
			
			
		else:
			#velocity control
			self.velocityControl(vDesired)
			