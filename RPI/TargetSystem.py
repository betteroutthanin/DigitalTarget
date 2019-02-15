from Base import Base
from DTCamera import DTCamera
from ShotDetector import ShotDetector
from TargetDB import TargetDB
from ShotProcessor import ShotProcessor
from WebServer import WebServer
from Buttons import Buttons
from ADBridge import ADBridge
import time
import skimage

from States.State_MainMenu import State_MainMenu

class TargetSystem(Base):
    ##############################################################
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "TargetSystem"

        self.dtCamera = False
        self.shotDetector = False
        self.targetDB = False
        self.shotProcessor = False
        self.webServer = False
        self.buttons = False
        
        self.stateLast = False
        self.stateCurrent = False
        self.adBridge = False
        
        self.bb.Set("main", self)

    def Boot(self):
        self.ResetLogFile()
        self.LogMe("=============================")
        self.LogMe("==== Booting Main System ====")        
        self.LogMe("=============================")
        self.LogMe("Using skimage version " + skimage.__version__)
        
        # Set up all the goodies
        self.webServer = WebServer()
        self.webServer.AddCommand('<div id="_menu"></div><div id="_top"><h1>Booting</h1></div><div id="_mid"></div><div id="_bot"></div>')        
        
        self.dtCamera = DTCamera()
        self.dtCamera.DumpCameraSettings()        
        self.buttons = Buttons()        
        self.shotDetector = ShotDetector()        
        self.targetDB = TargetDB()        
        self.shotProcessor = ShotProcessor()
        self.adBridge = ADBridge()
        
        # Blackboard
        self.bb.Set("shotDetector", self.shotDetector)
        self.bb.Set("adBridge", self.adBridge)
        
        # Clean the page
        self.webServer.AddCommand('<div id="_top"></div><div id="_mid"></div><div id="_bot"></div>')        
        
        # Create the base state
        self.stateCurrent = State_MainMenu()
        
        # Load the "Current" target from disk
        self.targetDB.LoadTargetFromDisk("Current")
        
        # force update via AD
        self.adBridge.SendADBootCommands()
        
        self.LogMe("=============================")

    def Loop(self):
        self.LogMe("++++++++++++++++++++++++++++")
        self.LogMe("++++ Entering Main Loop ++++")
        
        #self.dtCamera.TakePhoto()
        #self.shotProcessor.ProcessShot(self.dtCamera.npBuffer, 10)
        # self.targetDB.ShowTarget("ram")
        
        inMainLoop = True
        while inMainLoop:
            
            # State change time
            if self.stateCurrent != self.stateLast:
                # only call the exit on valid state object
                if self.stateLast != False:
                    self.stateLast.OnExit()
                
                # OnEntry needed since we have a state change
                self.stateCurrent.OnEntry()
            
            self.stateLast = self.stateCurrent
            
            # tick tock
            #timeStart = time.time()
            self.stateCurrent = self.stateCurrent.Tick()
            #print((time.time() - timeStart) * 1000 * 1000)
            
            # keep the bridge between AD and RPI valid
            self.adBridge.Tick()
            
            # Full exit if needed - needs to be the last thing we do            
            if self.stateCurrent == False:
                self.LogMe("Main loop final exit invoked")
                inMainLoop = False
            
            
        
        #### end main lop
        
        self.LogMe("++++ Exiting Main Loop ++++")
        self.LogMe("+++++++++++++++++++++++++++")
            
        
        
