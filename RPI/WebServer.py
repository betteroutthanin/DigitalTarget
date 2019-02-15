import Config
from BlackBoard import BlackBoard
from Base import Base

import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs


class WebServer(Base):
    ##############################################################    
    def __init__(self):
        super(WebServer, self).__init__()
        self.loggingPrefix = "WebServer"
        
        self.commandBuffer = []
        self.lastCommand = False
        self.cleanBoot = True
        self.snapShotPoint = 0
                
        self.wst = WebServerThread().start()
        
        self.LogMe("Booted")
    
    ##############################################################
    def getNextCommand(self):
        if len(self.commandBuffer) == 0:
            return False
        
        return self.commandBuffer.pop(0)
    
    ##############################################################
    def MakeCommandBufferSnapShot(self):
        if len(self.commandBuffer) == 0:
            return False
        
        self.snapShotPoint = len(self.commandBuffer) - 1
    
    ##############################################################
    def getCommand(self, indexID):
        
        # Do nothing if there is nothing in the buffer
        if len(self.commandBuffer) == 0:
            return False
        
        # only send over new stuff
        if len(self.commandBuffer) > indexID:            
            return self.commandBuffer[indexID]
        
        return False

    ##############################################################
    def AddCommand(self, command):
        if command != self.lastCommand:
            self.commandBuffer.append(command)
            self.lastCommand = command

##############################################################        
class WebServerThread(threading.Thread, Base):
    def run (self):
        # __init__ replacement
        self.loggingPrefix = "WebServerThread"
        self.LogMe("Booting webserver thread")
        
        server_address = ('', 8081)
        # server_address = ('*', 8081)
        httpd = HTTPServer(server_address, WebSereverRequestHandler)        
        httpd.serve_forever()

##############################################################            
class WebSereverRequestHandler(BaseHTTPRequestHandler, Base): 
    # not ideal, but it will work
    authTokens = []

    ##############################################################
    def log_message(self, format, *args):
        # you must be quite - now!
        return
        
    ##############################################################
    def ProcessPage(self):
        # self.LogMe("Processing page")
        # Make sure there is a page to server
        finalPath = self.pathData.path        
        if self.pathData.path.lower().endswith(("/")):
            finalPath = self.pathData.path + "index.html"

        filePath =  Config.webSitePath + finalPath
        self.LogMe("*** " + filePath)        
        
        message = self.FileGetContents(filePath);    
        
        if message == False:
            self.LogMe("page not found")
            return
        
        self.SendSimplePage(message)
        
    ##############################################################
    def ProcessImage(self):
        # self.LogMe("Processing image")
        filePath =  Config.webSitePath + self.pathData.path
        # self.LogMe("*** " + filePath)     
        
        imageContents = self.FileGetContentsBinMode(filePath)
        if imageContents == False:
            self.LogMe("Failed to find image " + filePath)     
            return
        
        self.send_response(200)        
        self.send_header('Content-type:', ' image/png')
        self.end_headers()        
        self.wfile.write(imageContents)
        
    ##############################################################
    def ProcessSound(self):
        # self.LogMe("Processing image")
        filePath =  Config.webSitePath + self.pathData.path
        # self.LogMe("*** " + filePath)     
        
        soundContents = self.FileGetContentsBinMode(filePath)
        if soundContents == False:
            self.LogMe("Failed to find sound " + filePath)     
            return
        
        self.send_response(200)        
        self.send_header('Content-type:', ' image/mpeg')
        self.end_headers()        
        self.wfile.write(soundContents)
        
    ##############################################################    
    def ProcessCSS(self):
        # self.LogMe("Processing CSS")
        filePath =  Config.webSitePath + self.pathData.path
        
        contents = self.FileGetContents(filePath)        
        if contents == False:
            return
        
        self.send_response(200)        
        self.send_header('Content-type','text/css')
        self.end_headers()        
        self.wfile.write(contents.encode("utf-8"))
        
    ##############################################################
    def ProcessView(self):
        # call view based on outcome        
        finalPath = self.pathData.path.replace(".view", "")
        finalPath =finalPath.replace("/", "")        
        
        viewObjectName = "Views." + finalPath + "." + finalPath        
        viewObject = self.MillNewZobject(viewObjectName)        
        if viewObject == False:
            self.LogMe("Files to create view " + viewObjectName)
            return
        
        # ok you lazy shit - do some work    
        viewObject.RenderView(self)
        
        # todo - de we need to delete the milled object
        
    ##############################################################
    def ProcessAjax(self):
        finalPath = self.pathData.path.replace(".pax", "")
        finalPath =finalPath.replace("/", "")
           
        ajaxObjectName = "Ajax." + finalPath + "." + finalPath
        ajaxObject = self.MillNewZobject(ajaxObjectName)        
        if ajaxObject == False:
            self.LogMe("Filed to create ajax " + ajaxObjectName)
            return
        
        # ok you lazy shit - do some work    
        ajaxObject.ProcessAjax(self)
            
    ##############################################################        
    def SendSimplePage(self, message):
        self.send_response(200)        
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
    
    ##############################################################
    def do_GET(self):
        self.loggingPrefix = "WebSereverRequestHandler"
        
        # Convert the URL to something more useful
        self.pathData = urlparse(self.path)
        self.queryData = parse_qs(self.pathData.query)
        
        # Debug fun time
        #self.LogMe(self.server.server_name)                
        # self.LogMe(self.path)        
        #self.LogMe(self.pathData)
        # self.LogMe(self.queryData)
        
        # what sort of request are they making
        # /favicon.ico
        if self.pathData.path == "/favicon.ico":
            # do nothing
            # todo - work out a better way of handling this
            return
            
        # do this before we do the auth test
        if self.pathData.path.lower().endswith("authme"):
            self.ProcessAuth()
            return
        
        # At this point we are authed
        # image calls         
        if self.pathData.path.lower().endswith(('.png')):
            self.ProcessImage()
            return
        
        if self.pathData.path.lower().endswith(('.mp3')):
            self.ProcessSound()
            return

        # ajax calls            
        if self.pathData.path.lower().endswith(('.pax')):
            self.ProcessAjax()
            return
        
        # View calls
        if self.pathData.path.lower().endswith(('.view')):
            self.ProcessView()
            return
            
        # CSS calls
        if self.pathData.path.lower().endswith(('.css')):
            self.ProcessCSS()
            return
            
        # Finally - normal processing
        self.ProcessPage()
        return