#!/usr/bin/env python3
#Ben was here

















































#and here too

import wpilib
from wpilib_controller import PIDController
import math
import rev

'''There is a new PIDController that will be in 2020 robotpy wpilib and is much easier to use. It can be downloaded seperately
by first running 'py -3 -m pip install --upgrade pip' and then 'py -3 -m pip install wpilib-controller' to be able to use before
having the 2020 version of robotpy. To install on the robot, run 'py -3 -m pip download wpilib-controller -d pip_cache' while
connected to the internet and then 'robotpy-installer install-pip wpilib-controller' while connected to the robot. Further
information about the new controller can be found at https://robotpy-wpilib-controller.readthedocs.io/en/latest/'''

class MyRobot(wpilib.TimedRobot):
	def robotInit(self):
		#I got fed up with how long 'frontLeft, frontRight, etc.' looked
		#Drive motors
		self.flDriveMotor = rev.CANSparkMax(2, rev.MotorType.kBrushless)
		self.frDriveMotor = rev.CANSparkMax(1, rev.MotorType.kBrushless)
		self.rlDriveMotor = rev.CANSparkMax(7, rev.MotorType.kBrushless)
		self.rrDriveMotor = rev.CANSparkMax(5, rev.MotorType.kBrushless)
		self.driveMotors = (self.flDriveMotor, self.frDriveMotor, self.rlDriveMotor, self.rrDriveMotor)

		#Turn motors
		self.flTurnMotor = rev.CANSparkMax(3, rev.MotorType.kBrushless)
		self.frTurnMotor = rev.CANSparkMax(4, rev.MotorType.kBrushless)
		self.rlTurnMotor = rev.CANSparkMax(8, rev.MotorType.kBrushless)
		self.rrTurnMotor = rev.CANSparkMax(6, rev.MotorType.kBrushless)
		self.turnMotors = (self.flTurnMotor, self.frTurnMotor, self.rlTurnMotor, self.rrTurnMotor)

		#Turn encoders
		self.flTurnEncoder = self.flTurnMotor.getEncoder()
		self.frTurnEncoder = self.frTurnMotor.getEncoder()
		self.rlTurnEncoder = self.rlTurnMotor.getEncoder()
		self.rrTurnEncoder = self.rrTurnMotor.getEncoder()
		self.turnEncoders = (self.flTurnEncoder, self.frTurnEncoder, self.rlTurnEncoder, self.rrTurnEncoder)
		for encoder in self.turnEncoders:
			encoder.setPositionConversionFactor(20) #makes the encoder output in degrees

		'''We should use whichever encoder (built-in or absolute) gives the greatest results. If we use the absolute, easy. If 
		we use the build-in, the following will be an issue and a potential solution.
		
		Every time we turn off/on the robot, these encoders will read 0 and the absolute encoder will read the real value.
		I didn't do it here, but we will need a function that moves all the turn motors so that their positions are set to what
		the absolute encoder says it is. Something like
		for index, encoder in enumerate(self.turnEncoders):
			encoder.setPosition(self.absoluteEncoders[index]%360)
		because I've been using an unhealthy amount of for loops this reason. This would allow the auto to go from there, although
		the motors should have been zeroed beforehand. There would be a similar function that can be ran in teleop when a sufficiently
		out-of-the-way button is pressed so that we can automatically reset the motors to 0 when in the pits, something like
		for index, encoder in enumerate(self.turnEncoders):
			encoder.setPosition(self.absoluteEncoders[index]%360)
			self.turnControllers[index].setReference(0, rev.controlType.kPosition)
		that of course then removes itself from the queue once all four motor encoders are at 0 and all the absolute encoders are at 0.
		Despite a reset being available in the pits, we would still need to set the motor encoders to the absolute encoder positions
		to account for possible bumping, absent-minded turning, or in case we didn't have time to return to the pits and so were only
		able to reset the wheel positions by hand'''

		# PID coefficients
		self.kP = .0039
		self.kI = 0
		self.kD = 2.0e-6
		self.PIDTolerance = 1.0

		#PID controllers for the turn motors
		self.flTurnController = PIDController(self.kP, self.kI, self.kD)
		self.frTurnController = PIDController(self.kP, self.kI, self.kD)
		self.rlTurnController = PIDController(self.kP, self.kI, self.kD)
		self.rrTurnController = PIDController(self.kP, self.kI, self.kD)
		self.turnControllers = (self.flTurnController, self.frTurnController, self.rlTurnController, self.rrTurnController)
		for controller in self.turnControllers:
			controller.setTolerance(self.PIDTolerance)
			controller.enableContinuousInput(0, 360)
		
		self.joystick = wpilib.Joystick(0)
		self.joystickDeadband = .05
		self.timer = wpilib.Timer() #used to use it while testing stuff, don't need it now, but oh well
		
		self.robotLength = 10.0
		self.robotWidth = 10.0
	def encoderBoundedPosition(self, encoder):
		#I don't know if there's a set continuous for encoders, but it's easy enough to write
		position = encoder.getPosition()
		position %= 360
		if position < 0:
			position += 360
		return position
	def turnSpeedCalculator(self, i):
		speed = self.turnControllers[i].calculate(self.encoderBoundedPosition(self.turnEncoders[i]))
		if abs(speed) > 1:
			speed /= abs(speed)
		return speed
	def stopDriveMotors(self):
		for motor in self.driveMotors:
			motor.set(0)
		for motor in self.turnMotors:
			motor.set(0)
	def swerveMath(self, x, y, z):
		r = math.hypot(self.robotLength, self.robotWidth)
		
		a = x - z*(self.robotLength/r)
		b = x + z*(self.robotLength/r)
		c = y - z*(self.robotWidth/r)
		d = y + z*(self.robotWidth/r)
		
		flSpeed = math.hypot(b, c)
		frSpeed = math.hypot(b, d)
		rlSpeed = math.hypot(a, c)
		rrSpeed = math.hypot(a, d)
		
		maxSpeed = max(flSpeed, frSpeed, rlSpeed, rrSpeed)
		if maxSpeed > 1: #this way speed proportions are kept the same
			flSpeed /= maxSpeed
			frSpeed /= maxSpeed
			rlSpeed /= maxSpeed
			rrSpeed /= maxSpeed
		flAngle = math.degrees(math.atan2(b, c)) #works for all 4 quadrants
		frAngle = math.degrees(math.atan2(b, d))
		rlAngle = math.degrees(math.atan2(a, c))
		rrAngle = math.degrees(math.atan2(a, d))
		
		return (flSpeed, flAngle, frSpeed, frAngle, 
			rlSpeed, rlAngle, rrSpeed, rrAngle)
	def swerveDrive(self, x, y, z):
		speeds = self.swerveMath(x, y, z)
		if max(abs(x), abs(y), abs(z)) == 0:
			self.stopDriveMotors()
		else:
			for i in range(4):
			#checking whether to go to angle and drive forward or go to other side and drive backward
				position = self.encoderBoundedPosition(self.turnEncoders[i])
				goal = speeds[2*i+1]
				difference = abs(position - goal)
				if difference < 90 or difference > 270:
					self.turnControllers[i].setSetpoint(goal)
					self.driveMotors[i].set(speeds[2*i])
				else:
					if goal < 180:
						self.turnControllers[i].setSetpoint(goal + 180)
						self.driveMotors[i].set(-speeds[2*i])
					else:
						self.turnControllers[i].setSetpoint(goal - 180)
						self.driveMotors[i].set(-speeds[2*i])
				self.turnMotors[i].set(self.turnSpeedCalculator(i))
		
		'''I've been debating adding some checks to try and make this more efficient, but efficiency isn't
		super important right now and, more importantly, I don't really know python so anything I can think
		of would save minimal time (or possibly even make it take longer).'''
	def brakeMode(self):
		for motor in self.driveMotors:
			motor.setIdleMode(rev.IdleMode.kBrake)
		for motor in self.turnMotors:
			motor.setIdleMode(rev.IdleMode.kBrake)
	def coastMode(self):
		for motor in self.driveMotors:
			motor.setIdleMode(rev.IdleMode.kCoast)
		for motor in self.turnMotors:
			motor.setIdleMode(rev.IdleMode.kCoast)
	def checkDeadband(self, axis):
		if abs(axis) < self.joystickDeadband:
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
		x = self.checkDeadband(self.joystick.getX())
		y = self.checkDeadband(self.joystick.getY())
		z = self.checkDeadband(self.joystick.getZ())
		self.swerveDrive(x, y, z)
	def disabledInit(self):
		self.coastMode()

if __name__ == "__main__":
	wpilib.run(MyRobot)