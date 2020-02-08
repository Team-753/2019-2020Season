import wpilib
import math
import rev
from wpilib import controller as controller
from SwerveModule import SwerveModule

class DriveTrain:
	robotLength = 27.3
	robotWidth = 23.1
	
	def __init__(self):
		self.frontLeft = SwerveModule(5,6,2,51.75)
		self.frontRight = SwerveModule(1,2,0,37)
		self.rearLeft = SwerveModule(7,8,3,357.3)
		self.rearRight = SwerveModule(3,4,1,290)
		
	def move(self,x,y,z):
		a = x - z*self.robotLength/2
		b = x + z*self.robotLength/2
		c = y - z*self.robotWidth/2
		d = y + z*self.robotWidth/2
		
		frontLeftAngle = math.hypot(b,d)
		frontRightAngle = math.hypot(b,c)
		rearLeftAngle = math.hypot(a,d)
		rearRightAngle = math.hypot(a,c)
		
		frontLeftSpeed = math.atan2(b,d)
		frontRightSpeed = math.atan2(b,c)
		rearLeftSpeed = math.atan2(a,d)
		rearRightSpeed = math.atan2(a,c)
		
		maxSpeed = max(frontLeftSpeed,frontRightSpeed,rearLeftSpeed,rearRightSpeed)
		if maxSpeed > 1:
			frontLeftSpeed /= maxSpeed
			frontRightSpeed /= maxSpeed
			rearLeftSpeed /= maxSpeed
			rearRightSpeed /= maxSpeed
		
		self.frontLeft.move(frontLeftSpeed,frontLeftAngle)
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
		