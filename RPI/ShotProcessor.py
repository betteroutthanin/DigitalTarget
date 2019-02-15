from Base import Base
from TargetDB import TargetDB

import time

import numpy as np
from skimage.io import imread, imsave
from skimage.feature import blob_log, blob_doh
from skimage.color import rgb2gray
from skimage.measure import points_in_poly
from skimage import exposure
import matplotlib.pyplot as plt


class ShotProcessor(Base):
    ##############################################################
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "ShotProcessor"
    
    ##############################################################
    def ProcessShot(self, npImage, targetName, shotID):
        #self.LogMe("ProcessShot - Started")
        targetPoly = self.bb.Get("main").targetDB.GetTarget(targetName).polyData        
        
        # Highjack the image data
        # npImage = imread("lastPhoto.png")
     
        # Make it gray scale - needed for blob detection
        npImage = rgb2gray(npImage)       
        
        # This will darken the image and leave the laser dot . . . . we hope
        npImage = exposure.adjust_sigmoid(npImage, cutoff=0.90, gain=40)
        npImage = exposure.rescale_intensity(npImage)
        
        # look for the blob        
        #blobs = blob_log(npImage, max_sigma=5)    #Slow
        blobs = blob_doh(npImage, max_sigma=5)     #Quick
        
        # how many blobs is too many?
        blobCount = len(blobs)
        x = -1000
        y = -1000
        if blobCount != 1:
            self.LogMe("ProcessShot - odd blob count found = " + str(blobCount))
        
        # Did the shot hit
        if len(blobs) == 1:
            x = blobs[0][1]
            y = blobs[0][0]        
            # self.LogMe("shotX = " + str(x) + "  shotY = " + str(y))
                
        hit = points_in_poly(np.array([[y,x]]), targetPoly)        
        
        webResponse = self.BWC_ShotDetails(targetName, x, y, npImage, hit, shotID)
        webserver = self.bb.Get("main").webServer
        webserver.AddCommand(webResponse)
        
        render = False        
        targetOutlineData = []
        targetOutlineData.append(targetPoly)        
        if render:
            fig, ax = plt.subplots()
            ax.imshow(npImage, interpolation='nearest', cmap=plt.cm.gray)

            for n, contour in enumerate(targetOutlineData):
                ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

            ax.axis('image')
            ax.set_xticks([])
            ax.set_yticks([])
            plt.show()
            
        return hit
    
    ##############################################################
    def BWC_ShotDetails(self, targetName, shotX, shotY, shotImage, hit, shotID):
        
        target = self.bb.Get("main").targetDB.GetTarget(targetName)        
        canvasSizeX = target.sizeX
        canvasSizeY = target.sizeY 
        
        # ##########
        scriptShotData = '''
        // Cross hairs
        ctx.beginPath();        
        ctx.moveTo({shotX}, 0);
        ctx.lineTo({shotX}, {canvasSizeY});
        ctx.strokeStyle="#{shotFillColour}";
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.closePath();
        
        ctx.beginPath();        
        ctx.moveTo(0, {shotY});
        ctx.lineTo({canvasSizeX}, {shotY});
        ctx.strokeStyle="#{shotFillColour}";
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.closePath();        
        
        // Bullet hole
        ctx.beginPath();
        ctx.arc({shotX}, {shotY}, 3, 0, 2 * Math.PI);
        ctx.fillStyle="#{shotFillColour}";
        ctx.strokeStyle="#000000";
        ctx.stroke();
        ctx.fill();
        ctx.closePath();        
        '''
        
        if hit:
            scriptShotData = scriptShotData + '''
            var audio = new Audio('/Sounds/hit.mp3');
            audio.play();
            '''
        else:
            scriptShotData = scriptShotData + '''
            var audio = new Audio('/Sounds/miss.mp3');
            audio.play();
            '''
            
            
        # make to bullet hole match the outcome        
        shotFillColour = "00FF00" if hit else "FF0000"        
        
        scriptShotData = scriptShotData.format(shotX = shotX,
                                               shotY = shotY,
                                               shotFillColour = shotFillColour,
                                               canvasSizeX = canvasSizeX,
                                               canvasSizeY = canvasSizeY)
        # ##########
        targetWebData = target.BuildWebView(scriptShotData)               
            
        hitString = "Hit" if hit else "Miss"            
        botWebData = '<div id="_bot">'+hitString+' - Result for shot #'+str(shotID)+'</div>'

        # Final part
        buffer = targetWebData + botWebData
        
        # Final output
        return buffer
        
        
        
