import collections
from States.State import State
from shutil import copyfile
import Config

class State_LearnTarget(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_LearnTarget"
        
        self.stage = 0
        
        self.LogMe("Booted")
        
    ##############################################################
    def Tick_Custom(self):
        
        # Wait to take photo
        if self.stage == 0:            
            buttons = collections.OrderedDict()
            buttons['mainMenu'] = "Main Menu"
            buttons['proceed'] = "Proceed"
            self.buttons.BuildWebButtonDeck(buttons)
            
            self.webServer.AddCommand('<div id="_top">Learn Target</div><div id="_mid">Insert target plate and add light<br>Ckick "Proceed" to continue</div><div id="_bot"></div>')
            self.stage = 1
            return self
            
        if self.stage == 1:
            if self.buttons.ButtonWasPressed("proceed"):
                self.webServer.AddCommand('<div id="_mid">Processing . . . . Please hold</div>')
                self.main.dtCamera.TakePhoto()
                self.main.targetDB.LearnTarget("temp", self.main.dtCamera.npBuffer)
                self.stage = 2
                return self
        
        # show result
        if self.stage == 2:
            target = self.main.targetDB.GetTarget("temp")
            if target:
                webData = target.BuildWebView(showLastImage = True)
                self.webServer.AddCommand(webData)
                self.webServer.AddCommand('<div id="_bot">Click "ok" to keep - or "cancel" to redo</div>')
                self.stage = 3                                
                
                buttons = collections.OrderedDict()
                buttons['mainMenu'] = "Main Menu"
                buttons['ok'] = "Ok"
                buttons['cancel'] = "Cancel"
                self.buttons.BuildWebButtonDeck(buttons)
            else:
                self.webServer.AddCommand('<div id="_mid">Failed to build valid image - adjust light and try again</div>')
                self.stage = 1
            
            return self
        
        # wait for ok or cancel
        if self.stage == 3:
            if self.buttons.ButtonWasPressed("cancel"):
                self.stage = 0
                return self
            
            if self.buttons.ButtonWasPressed("ok"):
                self.webServer.AddCommand('<div id="_bot">Target saving . . . </div>')
                self.stage = 4
                
                buttons = collections.OrderedDict()
                buttons['mainMenu'] = "Main Menu"
                self.buttons.BuildWebButtonDeck(buttons)
                
                # copy the last photo to the current.png target file
                copyfile(Config.lastPhotoPath, Config.targetPath + "Current.png")
                
                # Load the new target from disk
                self.main.targetDB.LoadTargetFromDisk("Current")
                
                self.webServer.AddCommand('<div id="_bot">Target saved</div>')
                
                return self
            
        # all done, dead state
        if self.stage == 4:
            return self
        
        return self