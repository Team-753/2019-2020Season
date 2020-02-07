import wpilib
import math
import rev
from wpilib import controller as controller
import SwerveModule


class Drive:
	def __init__(self):
		
		conversion = .08877
		self.frontLeft = [5,6,2,51.75,conversion] #driveID,turnID,absEncoderID,encoderOffset,encoderConversion
		self.backLeft = [7,8,3,357.3,conversion]
		self.frontRight = [1,2,0,37,conversion]
		self.backRight = [3,4,1,290,conversion]
		
	def Move(x,y,z):
	
		#offsets found: no
		#Offset then conversion
		#in degrees
		conversion = .08877
		frontLeft = [5,6,2,51.75,conversion] #driveID,turnID,absEncoderID,encoderOffset,encoderConversion
		backLeft = [7,8,3,357.3,conversion]
		frontRight = [1,2,0,37,conversion]
		backRight = [3,4,1,290,conversion]
		
		robotLength = 27.3
		robotWidth = 23.1
	
	
		r = math.sqrt((robotLength**2)+(robotWidth**2))
		
		a = x - (z*(robotLength/r))
		b = x + (z*(robotLength/r))
		c = y - (z*(robotWidth/r))
		d = y + (z*(robotWidth/r))
		
		bRSpeed = math.hypot(a,d)
		bLSpeed = math.hypot(a,c)
		fLSpeed = math.hypot(b,c)
		fRSpeed = math.hypot(b,d)
		
		bRAngle = math.atan2(a,d)*180/math.pi
		bLAngle = math.atan2(a,c)*180/math.pi
		fLAngle = math.atan2(b,d)*180/math.pi
		fRAngle = math.atan2(b,c)*180/math.pi
		
		SwerveModule.SwerveModule.Module(frontLeft[0],frontLeft[1],frontLeft[2],frontLeft[3],frontLeft[4],fLSpeed,fLAngle)
		
		SwerveModule.SwerveModule.Module(backLeft[0],backLeft[1],backLeft[2],backLeft[3],backLeft[4],bLSpeed,bLAngle)
		
		SwerveModule.SwerveModule.Module(frontRight[0],frontRight[1],frontRight[2],frontRight[3],frontRight[4],fRSpeed,fRAngle)
		
		SwerveModule.SwerveModule.Module(backRight[0],backRight[1],backRight[2],backRight[3],backRight[4],bRSpeed,bRAngle)
		
	def getEncoders():
		conversion = .08877
		frontLeft = [5,6,2,51.75,conversion] #driveID,turnID,absEncoderID,encoderOffset,encoderConversion
		backLeft = [7,8,3,357.3,conversion]
		frontRight = [1,2,0,37,conversion]
		backRight = [3,4,1,290,conversion]
		
		return('front left encoder at ' + str(frontLeft[4]*wpilib.AnalogInput(frontLeft[2]).getValue()+frontLeft[3]) + ' backLeft at ' + str(backLeft[4]*wpilib.AnalogInput(backLeft[2]).getValue()+backLeft[3]) + ' frontRight at ' + str(frontRight[4]*wpilib.AnalogInput(frontRight[2]).getValue()+frontRight[3]) + ' backRight at ' + str(backRight[4]*wpilib.AnalogInput(backRight[2]).getValue()+backRight[3]))
	