import collections
from States.State import State
import Config

stage_SetUp = 0
stage_WaitForAdjust = 1

class State_Settings(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_Settings"
        
        self.stage = stage_SetUp
        
        self.knockValue = int(self.FileGetContents(Config.knockValuePath))
        self.laserDelayValue = int(self.FileGetContents(Config.laserDelayValuePath))
                
        self.LogMe("Booted")       
        
    ##############################################################
    def OnExit_Custom(self):
        # force the laser off of exit
        self.bb.Get("adBridge").SendCommand("LS:off")
        
    ##############################################################
    def Tick_Custom(self):
    
        mid = self.BuildMidView()
    
        if self.stage == stage_SetUp:
            buttons = collections.OrderedDict()
            buttons['mainMenu'] = "Main Menu"
            buttons['save'] = "Save"
            self.buttons.BuildWebButtonDeck(buttons)
            
            message = ""
            message = message + '<div id="_top">Settings</div>'
            message = message + '<div id="_mid">' + mid + '</div>'
            message = message + '<div id="_bot"></div>'
            self.webServer.AddCommand(message)            
            self.stage = stage_WaitForAdjust
            return self
        
        if self.stage == stage_WaitForAdjust:
            message = '<div id="_mid">' + mid + '</div>'
            self.webServer.AddCommand(message)
            
            ### Knock value
            if self.buttons.ButtonWasPressed("knockDec"):
                self.knockValue = self.knockValue - 1
                if self.knockValue < 0 : self.knockValue = 0
                
            if self.buttons.ButtonWasPressed("knockInc"):
                self.knockValue = self.knockValue + 1
                if self.knockValue > 255 : self.knockValue = 255
            
            ### Laser delay
            if self.buttons.ButtonWasPressed("delayDec"):
                self.laserDelayValue = self.laserDelayValue - 1
                if self.laserDelayValue < 20 : self.laserDelayValue = 20
                
            if self.buttons.ButtonWasPressed("delayInc"):
                self.laserDelayValue = self.laserDelayValue + 1
                if self.laserDelayValue > 255 : self.laserDelayValue = 255
            
            ### Laser on / off
            if self.buttons.ButtonWasPressed("laserOff"):                
                self.bb.Get("adBridge").SendCommand("LS:off")
            
            if self.buttons.ButtonWasPressed("laserOn"):                
                self.bb.Get("adBridge").SendCommand("LS:on")
            
            ### Save (ignore laser on /off)
            if self.buttons.ButtonWasPressed("save"):
                self.bb.Get("adBridge").SendCommand("KS:" + str(self.knockValue))
                self.FilePutContents(Config.knockValuePath, str(self.knockValue))        
                
                self.bb.Get("adBridge").SendCommand("TS:" + str(self.laserDelayValue))
                self.FilePutContents(Config.laserDelayValuePath, str(self.laserDelayValue))        
            
            return self        
        return self
        
    ##############################################################
    def BuildMidView(self):
        entries = []
        
        ### Knock value
        knock = []
        knock.append(self.buttons.BuildWebButton("knockDec", "-"))
        knock.append("Knock senitivity = " + str(self.knockValue))
        knock.append(self.buttons.BuildWebButton("knockInc", "+"))
        entries.append(knock)
        
        ### Knock value
        delay = []
        delay.append(self.buttons.BuildWebButton("delayDec", "-"))
        delay.append("Laser delay value (ms) = " + str(self.laserDelayValue))
        delay.append(self.buttons.BuildWebButton("delayInc", "+"))
        entries.append(delay)
        
        ### Laser on / off
        laser = []
        laser.append(self.buttons.BuildWebButton("laserOff", "Off"))        
        laser.append("Laser test")
        laser.append(self.buttons.BuildWebButton("laserOn", "On"))        
        entries.append(laser)
        
        # Build the table
        buffer = ""        
        buffer += '<table style="width:100%">'
        for entry in entries:
            buffer += '<tr>'
            for bit in entry:
                buffer += '<td width="30%">'
                buffer += bit
                buffer += "</td>"
            buffer += "</tr>"
        buffer += "</table>"
        return buffer