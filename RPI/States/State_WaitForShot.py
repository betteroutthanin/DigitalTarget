from States.State import State

class State_WaitForShot(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_WaitForShot"
        
        self.shotID = 1
        self.maxShots = 5
        
        self.sleepTimeSec = 0.00001
        
        self.LogMe("Booted")
    
    ##############################################################
    def Tick_Custom(self):
        #self.LogMe("Tick_Custom - ")
        
        # Tell the user we are waiting for them
        self.main.webServer.AddCommand('<div id="_top">Waiting for shot to be made #'+ str(self.shotID) +'</div>')
        
        #takeShot = self.buttons.ButtonWasPressed("webShot")
        takeShot = self.bb.Get("shotDetector").TestForShot()
        if takeShot:
        
            self.main.dtCamera.TakePhoto()
            # main.targetDB.LearnTarget("chicken", main.dtCamera.npBuffer)
            
            self.main.webServer.AddCommand('<div id="_top">Processing Shot  #'+ str(self.shotID) +'</div>')
            self.main.shotProcessor.ProcessShot(self.main.dtCamera.npBuffer, "chicken", self.shotID)
            
            self.shotID = self.shotID + 1
                
        #sl = self.MillState("States.State_SleepLoop.State_SleepLoop")
        #return sl
        
        return self