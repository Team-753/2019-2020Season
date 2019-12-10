  
import wpilib
import math
import rev


class MyRobot(wpilib.TimedRobot):
	
	def robotInit(self):
   		self.kP = 0.03
		self.kI = 0.00
		self.kD = 0.00
		self.kF = 0.00
		
		self.exampleButton = 7
		
		#Sets up your PID controller with set constants
		self.controller = PIDController(self.kP, self.kI, self.kD)
		
		#set the range of values the Input will give
		#spark max are 42counts per revolution
		self.controller.enableContinuousInput(0, 4096)
		
		#you can find information about the motor stuff in the documentation
		self.PID_speed = self.controller.calculate(rev.CANSparkMax(4,rev.MotorType.kBrushless).getEncoder())

		
		
	def autonomousInit(self):
		pass
	def autonomousPeriodic(self):
		pass
	



		
	def teleopInit(self):
		pass
	def teleopPeriodic(self):
		#use this to control the motor: rev.CANSparkMax(4,rev.MotorType.kBrushless).set(0.5)
		if self.auxiliary1.getRawButton(self.exampleButton):
			self.controller.setpoint(84)
		else:
			rev.CANSparkMax(4,rev.MotorType.kBrushless).set(self.PID_speed)
		
		
		
if __name__ == '__main__':
	wpilib.run(MyRobot)
