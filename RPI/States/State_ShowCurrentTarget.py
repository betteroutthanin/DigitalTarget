import collections
from States.State import State

class State_ShowCurrentTarget(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_ShowCurrentTarget"   
        self.LogMe("Booted")
        
    ##############################################################
    def OnEntry_Custom(self):        
        buttons = collections.OrderedDict()
        buttons['mainMenu'] = "Main Menu"
        self.buttons.BuildWebButtonDeck(buttons)
        
        self.webServer.AddCommand('<div id="_top">Current Target</div><div id="_mid"></div><div id="_bot"></div>')
        target = self.main.targetDB.GetTarget("Current")
        webData = target.BuildWebView()
        self.webServer.AddCommand(webData)