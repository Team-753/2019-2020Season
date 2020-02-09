import wpilib
import math
import rev
from wpilib import controller as controller
from SwerveModule import SwerveModule

class DriveTrain:
	robotLength = 27.3
	robotWidth = 23.1
	diagonal = math.hypot(robotLength,robotWidth)
	
	def __init__(self):
		self.frontLeft = SwerveModule(5,6,2,???) #drive ID, turn ID, encoder ID, encoder offset
		self.frontRight = SwerveModule(1,2,0,???)
		self.rearLeft = SwerveModule(7,8,3,???)
		self.rearRight = SwerveModule(3,4,1,???)
		
	def move(self,x,y,z):
		a = x - z*self.robotLength/self.diagonal
		b = x + z*self.robotLength/self.diagonal
		c = y - z*self.robotWidth/self.diagonal
		d = y + z*self.robotWidth/self.diagonal
		
		frontLeftSpeed = math.hypot(b,d)
		frontRightSpeed = math.hypot(b,c)
		rearLeftSpeed = math.hypot(a,d)
		rearRightSpeed = math.hypot(a,c)
		
		frontLeftAngle = math.atan2(b,d)*180/math.pi #returns -180 to 180
		frontRightAngle = math.atan2(b,c)*180/math.pi
		rearLeftAngle = math.atan2(a,d)*180/math.pi
		rearRightAngle = math.atan2(a,c)*180/math.pi
		
		maxSpeed = max(frontLeftSpeed,frontRightSpeed,rearLeftSpeed,rearRightSpeed)
		if maxSpeed > 1:
			frontLeftSpeed /= maxSpeed
			frontRightSpeed /= maxSpeed
			rearLeftSpeed /= maxSpeed
			rearRightSpeed /= maxSpeed
		
		self.frontLeft.move(frontLeftSpeed,frontLeftAngle) #speed, angle
		self.frontRight.move(frontRightSpeed,frontRightAngle)
		self.rearLeft.move(rearLeftSpeed,rearLeftAngle)
		self.rearRight.move(rearRightSpeed,rearRightAngle)
		
	def stationary(self):
		self.frontLeft.stationary()
		self.frontRight.stationary()
		self.rearLeft.stationary()
		self.rearRight.stationary()
		
	def zeroEncoders(self):
		self.frontLeft.zeroEncoder()
		self.frontRight.zeroEncoder()
		self.rearLeft.zeroEncoder()
		self.rearRight.zeroEncoder()
		
	def coast(self):
		self.frontLeft.coast()
		self.frontRight.coast()
		self.rearLeft.coast()
		self.rearRight.coast()
		
	def brake(self):
		self.frontLeft.brake()
		self.frontRight.brake()
		self.rearLeft.brake()
		self.rearRight.brake()
		