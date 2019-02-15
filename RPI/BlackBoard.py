from Singleton import Singleton

@Singleton
class BlackBoard():
    ##############################################################
    def __init__(self):
        self.loggingPrefix = "BlackBoard"
        self.list = {}        

        self.LogMe("Created")

    ##############################################################
    def LogMe(self, message):
        print("- " + self.loggingPrefix + ":" + str(message))
    
    ##############################################################
    def CleanUp(self):                
        self.list = {}
        
    ##############################################################
    def DumpList(self):
        self.LogMe("List of things on the BB")
        self.LogMe(self.list)

    ##############################################################    
    def Remove(self, name):
        # todo
        pass

    ##############################################################
    def Get(self, name):
        if name in self.list:
            return self.list[name]
        return False

    ##############################################################
    def Set(self, name, object):
        if name in self.list:
            #self.LogMe("!!!! Item already in BlackBoard, this will override entry")
            pass
        self.list[name] = object
        # self.LogMe(name + " - Added -> " + str(object))
        
        return object