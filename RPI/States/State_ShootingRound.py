import collections
from States.State import State
import time

# defines
stage_SetUp = 0
stage_WaitToProceed = 1
stage_CountDown = 2
stage_PrepForShot = 3
stage_WaitingForShots = 4
stage_ProcessingShot = 5
stage_HoldTheEnd = 6
stage_SummarySetUp = 9
stage_Summary = 10

class State_ShootingRound(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_ShootingRound"

        self.stage = stage_SetUp
        self.shotID = 1
        self.hitLog = []

        self.maxShots = 5
        self.countDownSec = 5
        self.holdEndTimeSec = 10
        self.timeForShotsSec = 30 * self.maxShots

        self.startTimeGeneric = 0

        self.sleepTimeSec = 0.00001

        self.LogMe("Booted")
    
    ##############################################################
    def Tick_Custom(self):
        # Set up
        if self.stage == stage_SetUp:            
            message = ""
            message = message + '<div id="_top">Shooting Round (' + str(self.maxShots) + ' Shots)</div>'
            message = message + '<div id="_mid"><br>You have ' + str(self.timeForShotsSec) + ' seconds to make all the shots<br><br>'
            message = message + 'Press Proceed to start</div>'
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
                buttons = collections.OrderedDict()
                buttons['mainMenu'] = "Main Menu"
                self.buttons.BuildWebButtonDeck(buttons)
                
                self.startTimeGeneric = time.time()
                self.stage = stage_CountDown
                return self

        # Count down
        if self.stage == stage_CountDown:
            timePassed = time.time() - self.startTimeGeneric
            timeLeft = int(self.countDownSec - timePassed)

            if timeLeft < 0:                                
                self.startTimeGeneric = time.time()
                self.webServer.AddCommand('<div id="_mid"></div>')
                self.stage = stage_PrepForShot
                return self

            self.webServer.AddCommand('<div id="_mid">Get ready . . . ' + str(timeLeft) + '</div>')
            return self
            
        # Prep for shot
        if self.stage == stage_PrepForShot:
            self.webServer.AddCommand('<div id="_top">Waitng for shot  #(' + str(self.shotID) + ' to be made)</div>')            
            self.stage = stage_WaitingForShots            
            return self

        # Waiting for shots
        if self.stage == stage_WaitingForShots:
            timePassed = time.time() - self.startTimeGeneric
            timeLeft = self.timeForShotsSec - timePassed
        
            # have we run out of time
            if timeLeft < 0:                
                self.startTimeGeneric = time.time()
                self.webServer.AddCommand('<div id="_top">Time has run out</div>')
                self.stage = stage_HoldTheEnd
                return self
                
            if self.shotID > self.maxShots:                
                self.startTimeGeneric = time.time()
                self.webServer.AddCommand('<div id="_top">Last shot fired</div>')
                self.stage = stage_HoldTheEnd
                return self
                
            # check for button press
            # if self.buttons.ButtonWasPressed("webShot"):
            if self.bb.Get("shotDetector").TestForShot():
                self.main.dtCamera.TakePhoto()                                
                self.main.webServer.AddCommand('<div id="_top">Processing Shot  #'+ str(self.shotID) +'</div>')
                self.stage = stage_ProcessingShot                                
                return self
        
            return self
        
        # Shot processing
        if self.stage == stage_ProcessingShot:
            hit = self.main.shotProcessor.ProcessShot(self.main.dtCamera.npBuffer, "Current", self.shotID)            
            self.shotID = self.shotID + 1
            self.hitLog.append(hit)
            self.stage = stage_PrepForShot
            return self
        
        # Hold the end
        if self.stage == stage_HoldTheEnd:            
            timePassed = time.time() - self.startTimeGeneric
            timeLeft = self.holdEndTimeSec - timePassed
            if timeLeft < 0:
                self.stage = stage_SummarySetUp
                return self
            
        
        # summary set up
        if self.stage == stage_SummarySetUp:            
            buttons = collections.OrderedDict()
            buttons['mainMenu'] = "Main Menu"
            self.buttons.BuildWebButtonDeck(buttons)

            shotCounter = 1
            midData = '<div id="_mid"> Outcomes for shoot<br>'
            for hit in self.hitLog:
                midData = midData + str(shotCounter) + "-" + ("Hit" if hit else "Miss")
                midData = midData + '<br>'
                shotCounter = shotCounter +1                
            midData = midData + '</div>'            
            self.main.webServer.AddCommand('<div id="_top">Summary of shoot</div>' + midData + '<div id="_bot"></div>')
            self.stage = stage_Summary                   
        
        # Summary stage - just spin the wheels
        if self.stage == stage_Summary:
            return self

        return self
