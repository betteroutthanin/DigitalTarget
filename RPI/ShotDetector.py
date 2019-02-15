from Base import Base
import RPi.GPIO as GPIO

class ShotDetector(Base):
    ##############################################################
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "ShotDetector"
        
        self.shotPin = 11
        GPIO.setmode(GPIO.BOARD)  # Pins
        GPIO.setup(self.shotPin, GPIO.IN)
        
        self.buttons = self.bb.Get("buttons")
        
        self.LogMe("Booted")

    ##############################################################
    def TestForShot(self):
        if self.buttons.ButtonWasPressed("webShot"): return True
        return GPIO.input(self.shotPin)
    
