import collections
from States.State import State
import Config

class State_ShowLog(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_ShowLog"   
        self.LogMe("Booted")
        
    ##############################################################
    def OnEntry_Custom(self):                
        buttons = collections.OrderedDict()
        buttons['mainMenu'] = "Main Menu"
        self.buttons.BuildWebButtonDeck(buttons)
        
        self.webServer.AddCommand('<div id="_top">Log file</div><div id="_mid"></div><div id="_bot"></div>')
        
        logFileContents = self.FileGetContents(Config.logPath)
        webData = '<div id="_mid"><div class="log"><pre>' + logFileContents + '</pre></div></div>'
        self.webServer.AddCommand(webData)