#!/usr/bin/env python3

#Example change

import wpilib
from wpilib_controller import PIDController
import math
import rev

'''There is a new PIDController that will be in 2020 robotpy wpilib and is much easier to use. It can be downloaded seperately
by first running 'py -3 -m pip install --upgrade pip' and then 'py -3 -m pip install wpilib-controller' to be able to use before
having the 2020 version of robotpy. To install on the robot, run 'py -3 -m pip download wpilib-controller -d pip_cache' while
connected to the internet and then 'py -3 installer.py install-pip wpilib-controller' while connected to the robot. Further
information about the new controller can be found at https://robotpy-wpilib-controller.readthedocs.io/en/latest/'''

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		self.driveMotor = rev.CANSparkMax(1, rev.MotorType.kBrushless)
		self.turnMotor = rev.CANSparkMax(4, rev.MotorType.kBrushless)
		self.turnEncoder = self.turnMotor.getEncoder()
		self.turnEncoder.setPositionConversionFactor(20)

		# PID coefficients
		self.kP = .0039
		self.kI = 2e-6
		self.kD = 0

		#PID controllers for the turn motors
		self.turnController = PIDController(self.kP, self.kI, self.kD)
		self.PIDTolerance = 1.0
		self.turnController.setTolerance(self.PIDTolerance)
		self.turnController.enableContinuousInput(0, 360)
		
		self.joystick = wpilib.Joystick(0)
		self.joystickDeadband = .1
		self.timer = wpilib.Timer() #used to use it while testing stuff, don't need it now, but oh well
		
		self.robotLength = 10.0
		self.robotWidth = 10.0
		wpilib.CameraServer.launch()
	def encoderBoundedPosition(self, encoder):
		#I don't know if there's a set continuous for encoders, but it's easy enough to write
		position = encoder.getPosition()
		position %= 360
		if position < 0:
			position += 360
		return position
	def turnSpeedCalculator(self):
		speed = self.turnController.calculate(self.encoderBoundedPosition(self.turnEncoder))
		if abs(speed) > 1:
			speed /= abs(speed)
		return speed
	def swerveMath(self, x, y):
		driveSpeed = math.hypot(x, y)
		driveSpeed = min(driveSpeed, 1)
		angle = math.degrees(math.atan2(x, y)) #works for all 4 quadrants
		return (driveSpeed, angle)
	def swerveDrive(self, x, y):
		speeds = self.swerveMath(x, y)
		if max(abs(x), abs(y)) == 0:
			self.driveMotor.set(0)
			self.turnMotor.set(0)
		else:
			#checking whether to go to angle and drive forward or go to other side and drive backward
			position = self.encoderBoundedPosition(self.turnEncoder)
			goal = speeds[1]
			difference = abs(position - goal)
			if difference < 90 or difference > 270:
				self.turnController.setSetpoint(goal)
				self.driveMotor.set(speeds[0])
			else:
				if goal < 180:
					self.turnController.setSetpoint(goal + 180)
					self.driveMotor.set(-speeds[0])
				else:
					self.turnController.setSetpoint(goal - 180)
					self.driveMotor.set(-speeds[0])
		self.turnMotor.set(self.turnSpeedCalculator())
		
		'''I've been debating adding some checks to try and make this more efficient, but efficiency isn't
		super important right now and, more importantly, I don't really know python so anything I can think
		of would save minimal time (or possibly even make it take longer).'''
	def brakeMode(self):
		self.driveMotor.setIdleMode(rev.IdleMode.kBrake)
		self.turnMotor.setIdleMode(rev.IdleMode.kBrake)
	def coastMode(self):
		self.driveMotor.setIdleMode(rev.IdleMode.kCoast)
		self.turnMotor.setIdleMode(rev.IdleMode.kCoast)
	def checkDeadband(self, axis):
		if axis < self.joystickDeadband and axis > -self.joystickDeadband:
			axis = 0
		return axis
	def autonomousInit(self):
		self.brakeMode()
		'''We want the motors in brake mode while we are actually using them, which would be anytime
		during auto or teleop. However, we want them in coast mode while disabled so that people can
		easily spin/adjust the wheels as needed. Not super important, but also not hard to add'''
	def autonomousPeriodic(self):
		pass
	def teleopInit(self):
		self.brakeMode()
	def teleopPeriodic(self):
		if self.joystick.getRawButton(1):
			x = -.4*self.checkDeadband(self.joystick.getX())
			y = -.4*self.checkDeadband(self.joystick.getY())
		else:
			x = -1*self.checkDeadband(self.joystick.getX())
			y = -1*self.checkDeadband(self.joystick.getY())
		self.swerveDrive(x, y)
	def disabledInit(self):
		self.coastMode()

if __name__ == "__main__":
	wpilib.run(MyRobot)