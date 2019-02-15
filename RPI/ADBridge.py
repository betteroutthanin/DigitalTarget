from Base import Base
import Config
import serial

class ADBridge(Base):
    ##############################################################
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "ADBridge"
        
        self.serialToAD = serial.Serial('/dev/ttyACM0', 9600, timeout = 0)
        
        self.LogMe("Booted")
    
    ##############################################################
    def SendCommand(self, command):
        # Clean up before we send - AD is very sensitive
        command = command.replace("\n", "")
        command = command.replace("\r", "")
        command = command + "\n"
        
        self.serialToAD.write(str.encode(command))
    
    ##############################################################
    def Tick(self):
        dataFromAD = self.serialToAD.readline()            
        if (len(dataFromAD)):            
            dataAsString = dataFromAD.decode("utf-8")
            # strip out carrage returns and line feeds
            dataAsString = dataAsString.replace("\n", "")
            dataAsString = dataAsString.replace("\r", "")
            
            self.LogMe("Data from AD = " + str(dataAsString))
            
            parts = dataAsString.split(":")
            if len(parts) == 2:
                
                # Booted? - send over the correct Knock Value
                if parts[0] == "Boot":
                    self.LogMe("Detected AD Booting - will send set up commands")
                    self.SendADBootCommands()                    
    
    ##############################################################
    def SendADBootCommands(self):
        knockSetCommand = "KS:" + self.FileGetContents(Config.knockValuePath)                    
        self.SendCommand(knockSetCommand)
        
        knockSetCommand = "TS:" + self.FileGetContents(Config.laserDelayValuePath)                    
        self.SendCommand(knockSetCommand)
            
            