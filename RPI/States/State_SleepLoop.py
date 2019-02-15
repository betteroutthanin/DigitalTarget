from States.State import State
import time
class State_SleepLoop(State):
    ##############################################################
    def __init__(self):
        State.__init__(self)
        self.loggingPrefix = "State_SleepLoop"
        
        self.LogMe("Booted")
    
    ##############################################################
    def Tick_Custom(self):
        time.sleep(10)        
        return self