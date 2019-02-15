import Config
from Ajax.Ajax import Ajax
import time

class Ajax_CommandBuffer(Ajax):
    ##############################################################
    def __init__(self):
        Ajax.__init__(self)
        self.loggingPrefix = "Ajax_CommandBuffer"
    
    ##############################################################
    def Process(self, requestHandler):
        contents = ""
        
        webServer = self.bb.Get("main").webServer
        
        # make sure the request ID is valid and present
        if "lastID" in requestHandler.queryData:
            lastIDVal = requestHandler.queryData['lastID'][0]
            lastIDVal = int(lastIDVal)
            
            # Skip the old stuff if there is a valid snapshot marker
            if lastIDVal < webServer.snapShotPoint:
                lastIDVal = webServer.snapShotPoint                
            
            if webServer.cleanBoot:
                lastIDVal = 0
                webServer.cleanBoot = False
            
            # print(lastIDVal) 
            command = webServer.getCommand(lastIDVal)
        
            if command:
                contents = command + '<div id="_lastID">' + str(lastIDVal + 1) + '</div>'

        requestHandler.SendSimplePage(contents)