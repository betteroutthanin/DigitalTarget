import Config
from Ajax.Ajax import Ajax
from BlackBoard import BlackBoard

class Ajax_Button(Ajax):
    ##############################################################
    def __init__(self):
        Ajax.__init__(self)
        self.loggingPrefix = "Ajax_button"
        
    def Process(self, requestHandler):                
        # was a button presses
        bb = BlackBoard.Instance()
        buttonName = False
        if "ButtonName" in requestHandler.queryData:
            buttonName = requestHandler.queryData['ButtonName'][0]
            bb.Get("buttons").PressButton(buttonName)
            # self.LogMe("Button was pressed + " + buttonName)        
        
        message = " "       
        requestHandler.SendSimplePage(message)