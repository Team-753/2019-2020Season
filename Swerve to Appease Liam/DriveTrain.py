import wpilib
import math
import rev
from wpilib import controller as controller
import SwerveModule.SwerveModule as SwerveModule

class DriveTrain:
	robotLength = 27.3
	robotWidth = 23.1
	
	def __init__(self):
		self.frontLeft = SwerveModule(5,6,2,51.75)
		self.frontRight = SwerveModule(1,2,0,37)
		self.rearLeft = SwerveModule(7,8,3,357.3)
		self.rearRight = SwerveModule(3,4,1,290)
		
	def drive(self,x,y,z):
		
		
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
		