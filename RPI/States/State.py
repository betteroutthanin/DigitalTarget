from Base import Base
import time

class State(Base):
    ##############################################################
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "State"
        
        self.sleepTimeSec = 0.10
        
        #self.LogMe("Booted")
        
    ##############################################################
    def __del__(self):
        #print("Dead, your god is dead " + self.loggingPrefix)
        pass
    
    ##############################################################
    ##############################################################
    def OnEntry_Custom(self):
        #self.LogMe("OnEntry_CustomOnEntry - Must be implemented")
        pass
    
    ##############################################################
    def OnExit_Custom(self):
        # self.LogMe("OnExit_Custom - Must be implemented")
        pass
    
    ##############################################################
    def Tick_Custom(self):
        #self.LogMe("Tick_Custom - Must be implemented")
        return self
    
    ##############################################################
    ##############################################################
    def OnEntry(self):
        #self.LogMe("OnEntry - ")
        self.buttons = self.bb.Get("buttons")
        self.main = self.bb.Get("main")
        self.webServer = self.main.webServer
        self.targetDB = self.main.targetDB
        
        self.OnEntry_Custom()
    
    ##############################################################
    def OnExit(self):
        #self.LogMe("OnExit - ")        
        self.OnExit_Custom()        
    
    ##############################################################
    def Tick(self):
        # self.LogMe("Tick - ")        
        # check to see if the main button has been presssed
        
        # force a main menu if we need to do it        
        if self.buttons.ButtonWasPressed("mainMenu"):
            return self.MillState("States.State_MainMenu.State_MainMenu")
        
        time.sleep(self.sleepTimeSec)
        
        return self.Tick_Custom()


    ##############################################################
    ##############################################################        
    def MillState(self, stateName):        
        m = self.GetClass(stateName)
        object = m()
        return object
        
    ##############################################################
    def GetClass(self, name):
        parts = name.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m