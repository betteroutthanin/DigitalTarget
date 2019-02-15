import collections
from States.State import State
import time

# defines
stage_SetUp = 0
stage_WaitToProceed = 1
stage_PrepForShot = 2
stage_WaitingForShots = 3
stage_ProcessingShot = 4

class State_OpenShoot(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_OpenShoot"
        
        self.stage = stage_SetUp
        self.shotCount = 0
        self.hitCount = 0
        
        self.sleepTimeSec = 0.00001
      
        self.LogMe("Booted")
    
    ##############################################################
    def Tick_Custom(self):

        # Set up
        if self.stage == stage_SetUp:            
            message = ""
            message = message + '<div id="_top">Open Shooting Round</div>'            
            message = message + '<div id="_mid">Press Proceed to start</div>'
            message = message + '<div id="_bot"></div>'
            self.webServer.AddCommand(message)

            buttons = collections.OrderedDict()
            buttons['mainMenu'] = "Main Menu"
            buttons['proceed'] = "Proceed"
            self.buttons.BuildWebButtonDeck(buttons)
            
            self.stage = stage_WaitToProceed
            return self

        # wait for the proceed
        if self.stage == stage_WaitToProceed:
            if self.buttons.ButtonWasPressed("proceed"):
                self.webServer.AddCommand('<div id="_mid"></div>')            
                
                buttons = collections.OrderedDict()
                buttons['mainMenu'] = "Main Menu"
                # buttons['webShot'] = "Web Shot"
                self.buttons.BuildWebButtonDeck(buttons)
                
                self.stage = stage_PrepForShot
                return self            
            
         # Prep for shot
        if self.stage == stage_PrepForShot:
            self.webServer.AddCommand('<div id="_top">Waitng for shot to be made</div>')            
            self.stage = stage_WaitingForShots            
            return self

        # Waiting for shots
        if self.stage == stage_WaitingForShots:                
            # check for button press
            # if self.buttons.ButtonWasPressed("webShot"):
            if self.bb.Get("shotDetector").TestForShot():
                self.main.dtCamera.TakePhoto()                                
                self.main.webServer.AddCommand('<div id="_top">Processing Shot</div>')
                self.stage = stage_ProcessingShot                                
                return self        
            return self
        
        # Shot processing
        if self.stage == stage_ProcessingShot:
            self.shotCount = self.shotCount + 1
            hit = self.main.shotProcessor.ProcessShot(self.main.dtCamera.npBuffer, "Current", self.shotCount)
            if hit:
                self.hitCount = self.hitCount + 1
                
            per = (self.hitCount / self.shotCount) * 100
            self.main.webServer.AddCommand('<div id="_bot">Count = ' + str(self.shotCount) + ' - Hit = ' + '{0:.2f}'.format(per) + '%</div>')
            self.stage = stage_PrepForShot
            return self

        return self
