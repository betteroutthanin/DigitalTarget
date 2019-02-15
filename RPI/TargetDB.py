import Config
from Base import Base
from Target import Target

import os.path
import glob

import numpy as np
from skimage.io import imread, imsave
from skimage import measure
from skimage.color import rgb2gray, grey2rgb
from skimage import util
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from skimage import feature
from skimage.draw import polygon, rectangle


class TargetDB(Base):
    ##############################################################
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "TargetDB"
        
        self.targetBasePath = Config.targetPath
        self.maxSections = 1
        
        # the main data store
        self.db = {}
        
        self.LogMe("Booted")
        
    ##############################################################
    def GetTarget(self, name):
        if name in self.db:
            return self.db[name]        
        
        return False;        
    
    ##############################################################
    def Boot(self):
        #self.buildAddDiskTargets()
        pass
    
    def LoadTargetFromDisk(self, targetName):
        imageData = imread(self.targetBasePath + targetName + ".png")
        self.LearnTarget(targetName, imageData)
        pass
    
    ##############################################################
    def LearnTarget(self, targetName, imageDataPassed):
        self.LogMe("LearnTarget - started - " + targetName)
        imageData = imageDataPassed
        
        # Process the image to get a nice bool image with the shape
        '''
        # This works for a full size image
        imageData = rgb2gray(imageData)
        imageData = util.invert(imageData)        
        edges = feature.canny(imageData, sigma=5)
        edges = ndi.binary_fill_holes(edges)
        '''
        
        # need a mask to filter out the light from the out edges
        mask = np.zeros([imageData.shape[0], imageData.shape[1]], dtype=np.uint8)
        
        rStart = int(imageData.shape[0] * .1)
        rEnd = int(imageData.shape[0] * .9)
        cStart = int(imageData.shape[1] * .1)
        cEnd = int(imageData.shape[1] * .9)
        
        start = (rStart, cStart)
        end = (rEnd, cEnd)
        rr, cc = rectangle(start, end=end, shape=mask.shape)
        mask[rr, cc] = 1
        mask = mask <= 0.5
        
        # This seems to work for a 1/3 size image
        # note the 5/3 for sigma
        imageData = rgb2gray(imageData)
        imageData = util.invert(imageData)        
        # edges = feature.canny(imageData, sigma = 5/3, mask = mask)
        edges = feature.canny(imageData, sigma = 5/3)
        edges = ndi.binary_fill_holes(edges)
        
        # Create the outline
        targetOutlineData = measure.find_contours(edges, 0.8)
        
        # add some support here
        count = len(targetOutlineData)
        self.LogMe("LearnTarget - Found outlines -> " + str(count))        
        
        if count > 0:
            largestData = 0
            largestCount = 0
            
            loopID = 0
            # find the largest one
            for subData in targetOutlineData:
                if len(subData) > largestCount:                    
                    largestCount = len(subData)
                    largestData = subData
                    # print (loopID)
                    # print (largestCount)
                    loopID = loopID + 1
            
            # Build and add the target
            targetData = Target()
            targetData.sizeX = imageData.shape[1]
            targetData.sizeY = imageData.shape[0]
            targetData.polyData = largestData
            
            self.db[targetName] = targetData

        # show the target if needed
        render = False        
        if render:
            outlineToRender = []
            outlineToRender.append(largestData)
            
            fig, ax = plt.subplots()
            ax.imshow(imageData, interpolation='nearest', cmap=plt.cm.gray)

            for n, contour in enumerate(outlineToRender):
                ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

            ax.axis('image')
            ax.set_xticks([])
            ax.set_yticks([])
            plt.show()