from Base import Base

class Ajax(Base):
    ##############################################################
    def __init__(self):        
        Base.__init__(self)
        self.loggingPrefix = "Ajax"
    
    ##############################################################
    def ProcessAjax(self, requestHandler):
        self.Process(requestHandler)