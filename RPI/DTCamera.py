from Base import Base
from picamera import PiCamera
from skimage.transform import rescale, rotate
from skimage.io import imsave
import numpy as np
import time
import Config

class DTCamera(Base):
    ##############################################################
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "DTCamera"
        
        self.lastImage = False
        
        self.cameraResWidth  = int(1200 / 3)
        self.cameraResHeight = int(1920 / 3)
        
        #self.cameraResWidth  = int(1200 / 1)
        #self.cameraResHeight = int(1920 / 1)           
        
        # pre built buffer for camera to capture to
        self.npBuffer = np.empty((self.cameraResHeight, self.cameraResWidth, 3), dtype=np.uint8)        
        
        # Core camera settings
        self.camera = PiCamera()
        
        self.camera.vflip = False
        self.camera.hflip = True
        self.camera.resolution = (self.cameraResWidth, self.cameraResHeight)
        
        # not sure what this does
        self.camera.shutter_speed = 0        
        
        self.camera.sensor_mode = 6
        self.camera.framerate = 15
        self.camera.iso = 0
        # self.camera.exposure_mode = 'sports'
        self.camera.exposure_compensation = 0
        self.camera.awb_mode = 'auto'
        self.useVideoPort = True
        self.camera.rotation = 90
        self.postRotation = 0
        self.postResize = 1
        
        # force a sleep to ensure the camera is settled
        time.sleep(3)
        self.LogMe("Booted")
    
    ##############################################################
    def DumpCameraSettings(self):
        self.LogMe("------ Camera settings ------")
        self.LogMe("resolution = " +            str(self.camera.resolution))
        self.LogMe("sensor_mode = " +           str(self.camera.sensor_mode))
        self.LogMe("exposure_mode = " +         str(self.camera.exposure_mode))
        self.LogMe("framerate = " +             str(self.camera.framerate))
        self.LogMe("exposure_speed = " +        str(self.camera.exposure_speed))
        self.LogMe("iso = " +                   str(self.camera.iso))
        self.LogMe("exposure_compensation = " + str(self.camera.exposure_compensation))
        self.LogMe("awb_mode = " +              str(self.camera.awb_mode))
        self.LogMe("useVideoPort = " +          str(self.useVideoPort))
        self.LogMe("rotation = " +              str(self.camera.rotation))
        self.LogMe("postRotation = " +          str(self.postRotation))
        self.LogMe("postResize = " +            str(self.postResize))
        self.LogMe("vflip = " +                 str(self.camera.vflip))
        self.LogMe("hflip = " +                 str(self.camera.hflip))
        self.LogMe("-----------------------------")
    
    ##############################################################
    def TakePhoto(self):        
        self.camera.capture(output = self.npBuffer, format = 'rgb', use_video_port = self.useVideoPort)
        imsave(Config.lastPhotoPath, self.npBuffer)                
    
    ##############################################################
    def ShowPhoto(self):        
        viewer = ImageViewer(self.npBuffer)
        viewer.show()
        