#!/usr/bin/env python3

import rev
import wpilib
from wpilib import controller as controller
import math

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		self.driveMotor = rev.CANSparkMax(1, rev.MotorType.kBrushless)
		self.turnMotor = rev.CANSparkMax(2, rev.MotorType.kBrushless)
		#self.turnEncoder = wpilib.AnalogInput(0)
		self.turnEncoder = self.turnMotor.getEncoder()
		self.turnEncoder.setPositionConversionFactor(20)

		# PID coefficients
		self.kP = 5e-5
		self.kI = 0
		self.kD = 0
		self.PIDTolerance = 0

		#PID controllers for the turn motors
		self.turnController = wpilib.controller.PIDController(self.kP, self.kI, self.kD)
		self.turnController.setTolerance(self.PIDTolerance)
		self.turnController.enableContinuousInput(0, 360)
		
		self.joystick = wpilib.Joystick(0)
		self.joystickDeadband = .05
		self.timer = wpilib.Timer() #used to use it while testing stuff, don't need it now, but oh well
		
		# Push PID Coefficients to SmartDashboard
		wpilib.SmartDashboard.putNumber("P Gain", self.kP)
		wpilib.SmartDashboard.putNumber("I Gain", self.kI)
		wpilib.SmartDashboard.putNumber("D Gain", self.kD)
		wpilib.SmartDashboard.putNumber("Set Rotations", 0)
		wpilib.SmartDashboard.putNumber("Tolerance", self.PIDTolerance)
		wpilib.SmartDashboard.putBoolean("Manual Control", True)
		wpilib.SmartDashboard.putNumber("Manual Speed", 0)
	def brakeMode(self):
		self.driveMotor.setIdleMode(rev.IdleMode.kBrake)
		self.turnMotor.setIdleMode(rev.IdleMode.kBrake)
	def coastMode(self):
		self.driveMotor.setIdleMode(rev.IdleMode.kCoast)
		self.turnMotor.setIdleMode(rev.IdleMode.kCoast)
	def getBoundedPosition(self, encoder):
		position = encoder.getPosition()
		position %= 360
		if position < 0:
			position += 360
		return position
	def turnSpeedCalculator(self):
		location = self.getBoundedPosition(self.turnEncoder)
		speed = self.turnController.calculate(location)
		return speed
	def autonomousInit(self):
		self.brakeMode()
	def autonomousPeriodic(self):
		pass
	def teleopInit(self):
		self.brakeMode()
	def teleopPeriodic(self):
		# Read data from SmartDashboard
		p = wpilib.SmartDashboard.getNumber("P Gain", self.kP)
		i = wpilib.SmartDashboard.getNumber("I Gain", self.kI)
		d = wpilib.SmartDashboard.getNumber("D Gain", self.kD)
		tolerance = wpilib.SmartDashboard.getNumber("Tolerance", self.PIDTolerance)
		test = wpilib.SmartDashboard.getBoolean("Manual Control", False)
		controlSpeed = wpilib.SmartDashboard.getNumber("Manual Speed", 0)

		# Update PIDController datapoints with the latest from SmartDashboard
		if p != self.kP:
			self.turnController.setP(p)
			self.kP = p
		if i != self.kI:
			self.turnController.setI(i)
			self.kI = i
		if d != self.kD:
			self.turnController.setD(d)
			self.kD = d
		if tolerance != self.PIDTolerance:
			self.turnController.setTolerance(tolerance)
			self.PIDTolerance = tolerance

		speed = self.turnSpeedCalculator()
		bob = self.getBoundedPosition(self.turnEncoder)
		wpilib.SmartDashboard.putNumber("Process Variable", bob)
		wpilib.SmartDashboard.putNumber("Me", bob)
		setpoint = wpilib.SmartDashboard.getNumber("Set Rotations", 0)
		self.turnController.setSetpoint(setpoint)
		wpilib.SmartDashboard.putNumber("Motor Input", speed)
		if test:
			self.turnMotor.set(controlSpeed)
		else:
			self.turnMotor.set(speed)
		
	def disabledInit(self):
		self.coastMode()

if __name__ == "__main__":
	wpilib.run(MyRobot)