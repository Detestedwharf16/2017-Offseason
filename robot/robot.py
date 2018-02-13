#!/usr/bin/env python3
import wpilib
import wpilib.drive
from networktables import NetworkTables
from Comms import Comm
from Actions import Drive
from Actions import Mandible
import Sensors
from Control import Toggle
from robotpy_ext.common_drivers.navx import AHRS
#from Control import Logic
import Auto

class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.table = NetworkTables.getTable("SmartDashboard")
        self.robot_drive = wpilib.drive.DifferentialDrive(wpilib.Spark(0), wpilib.Spark(1))
        self.stick = wpilib.Joystick(0)
        #self.climbingMotor = wpilib.Talon(2)
        #self.ballSwitch1 = wpilib.DigitalInput(4)
        #self.ballSwitch2 = wpilib.DigitalInput(5)
        #self.rightmandlible = Mandible( wpilib.Spark(2), wpilib.DigitalInput(0), wpilib.DigitalInput(1))
        #self.leftmandlible = Mandible( wpilib.Spark(3), wpilib.DigitalInput(2), wpilib.DigitalInput(3))
        #self.ballMotor1 = wpilib.Relay(0)
        self.ahrs = AHRS.create_i2c(0)
        #self.gearSpeed = .5
        #self.lights = wpilib.Relay(1)
        #self.lightToggle = False
        #self.lightToggleBool = True
        #self.togglev = 0
        self.wheel = wpilib.Encoder(0, 1)
        self.wheel2 = wpilib.Encoder(2, 3, True)
        self.encoder = Sensors.Encode(self.wheel, self.wheel2)
        #wpilib.CameraServer.launch()
        self.ultrasonic = wpilib.AnalogInput(0)
        self.autoSchedule = Auto.Auto() 
        self.elevatorMotor = wpilib.Talon(1)
    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.ahrs.reset()
        autoPicker = self.table.getNumber('auto', 0)
        config = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if autoPicker == 0:
            #starting from center go to the left of the scale
            if config[0] == 'L' :
                self.autoSchedule.addActions([Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 510, 0), Auto.Turn(self.ahrs, self.robot_drive, -90), Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 650, -90), Auto.Turn(self.ahrs, self.robot_drive, 0), Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 798, 0)])
            #starting from center go to right of the scale
            else:
                self.autoSchedule.addActions([Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 510, 0), Auto.Turn(self.ahrs, self.robot_drive, 90), Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 530, 90), Auto.Turn(self.ahrs, self.robot_drive, 0), Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 798, 0)])
        if autoPicker == 1:
            self.autoSchedule.addActions([Auto.Turn(self.ahrs, self.robot_drive, 90), Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 1700, 90), Auto.Turn(self.ahrs, self.robot_drive, 0), Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 1250, 0)])
        #starting in left position
        elif autoPicker == 2:
            if config[1] == ''
            self.autoSchedule.addActions([Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 600, 0), Auto.Turn(self.ahrs, self.robot_drive, -15), Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 600, -15), Auto.Turn(self.ahrs, self.robot_drive, 0), Auto.Forward(300, 20, self.ahrs, self.encoder, self.robot_drive, 2160, 0),Auto.Turn(self.ahrs, self.robot_drive, 90)])
        elif autoPicker == 3:
            self.autoSchedule.addActions([])
        elif autoPicker == 4:
            self.autoSchedule.addActions([])
        elif autoPicker == 5:
            self.autoSchedule.addActions([])
        elif autoPicker == 6:
            self.autoSchedule.addActions([])
        elif autoPicker == 7:
            self.autoSchedule.addActions([])

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        self.autoSchedule.update()
        self.table.putNumber('encodeD', self.wheel.getDistance())
        self.table.putNumber('encodeD2', self.wheel2.getDistance())
        self.table.putNumber('nav', self.ahrs.getYaw())

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.robot_drive.arcadeDrive(self.stick.getY(), self.stick.getX())
        if self.stick.getRawButton(5):
                self.elevatorMotor.set(0.5)  #make go uppy 
        elif self.stick.getRawButton(6):
                self.elevatorMotor.set(-0.5) #make go downy
        else:
                self.elevatorMotor.set(0)
        
        
#        if self.stick.getRawButton(1):
#            self.rightmandible.open()
#            self.leftmandible.open()
#        else:
#            self.rightmandible.close()
#            self.leftmandible.close()


        self.table.putNumber('encodeD', self.wheel.getDistance())
        self.table.putNumber('encodeD2', self.wheel2.getDistance())
        self.table.putNumber('nav', self.ahrs.getYaw())
        

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
