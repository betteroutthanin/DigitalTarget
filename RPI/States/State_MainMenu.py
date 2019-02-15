import collections
from States.State import State

class State_MainMenu(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_MainMenu"
        
        self.LogMe("Booted")
        
    ##############################################################
    def OnEntry_Custom(self):        
        self.webServer.MakeCommandBufferSnapShot()
        buttons = collections.OrderedDict()
        buttons['mainMenu'] = "Main Menu"
        buttons['showCurrentTarget'] = "Show Target"
        buttons['learnTarget'] = "Learn Target"
        buttons['shootingRound'] = "Shooting Round"
        buttons['openShoot'] = "Open Shoot"
        buttons['settings'] = "Settings"
        buttons['log'] =  "Logs"
        self.buttons.BuildWebButtonDeck(buttons)
        self.webServer.AddCommand('<div id="_top"><h1>Main Menu</h1></div><div id="_mid"></div><div id="_bot"></div>')
    
    ##############################################################
    def Tick_Custom(self):        
        
        # options        
        if self.buttons.ButtonWasPressed("shootingRound"):
            return self.MillState("States.State_ShootingRound.State_ShootingRound")
        
        if self.buttons.ButtonWasPressed("openShoot"):
            return self.MillState("States.State_OpenShoot.State_OpenShoot")
        
        if self.buttons.ButtonWasPressed("showCurrentTarget"):
            return self.MillState("States.State_ShowCurrentTarget.State_ShowCurrentTarget")
        
        if self.buttons.ButtonWasPressed("learnTarget"):
            return self.MillState("States.State_LearnTarget.State_LearnTarget")
        
        if self.buttons.ButtonWasPressed("settings"):
            return self.MillState("States.State_Settings.State_Settings")
        
        if self.buttons.ButtonWasPressed("log"):
            return self.MillState("States.State_ShowLog.State_ShowLog")
        
        return self