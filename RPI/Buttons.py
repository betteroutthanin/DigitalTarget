from Base import Base

class Buttons(Base):
    ##############################################################    
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "Buttons"

        self.buttonList = {}                
        
        self.bb.Set("buttons", self)        
        self.LogMe("Booted")
    
    ##############################################################
    def BuildWebButtonDeck(self, buttonDict):
        webServer = self.bb.Get("main").webServer
        
        guts = ""
        for buttonID in buttonDict:
            guts = guts + self.BuildWebButton(buttonID, buttonDict[buttonID])
        buffer = '<div id="_menu">' + guts + '</div>'        
        webServer.AddCommand(buffer)
        return True
    
    ##############################################################
    def BuildWebButton(self, buttonID, buttonText):
        buffer = ''' <button class="button" type="button" onclick="WebButton('{buttonID}')">{buttonText}</button> '''
        buffer = buffer.format(buttonID = buttonID, buttonText = buttonText)
        return buffer
    
    ##############################################################    
    def ButtonWasPressed(self, buttonName):
        # self.LogMe("ButtonWasPressed: Check = " + buttonName)
        if buttonName in self.buttonList:                        
            self.ClearAllButtons()
            return True
        
        return False
             
    ##############################################################    
    def PressButton(self, buttonName):
        #self.LogMe("PressButton: Name = " + buttonName)        
        self.buttonList[buttonName] = True
    
    ##############################################################
    def ClearAllButtons(self):
        self.buttonList = {}