from Base import Base
import random

class Target(Base):
    ##############################################################
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "Target"
        
        self.sizeX = 0
        self.sizeY = 0
        self.polyData =  []
        
    ##############################################################
    def GetPolyAsBuffer(self):
        buffer = ""
        for element in self.polyData:
            buffer = buffer + str(int(element[0])) + ":"
            buffer = buffer + str(int(element[1])) + "@"
        
        return buffer
        
        
    ##############################################################
    def BuildWebView(self, extraScript = "", showLastImage = False):
        canvasSizeX = self.sizeX
        canvasSizeY = self.sizeY
        
        targetPolyBuffer = self.GetPolyAsBuffer()
        
        # Setup + adding the poly data
        scriptTarget = '''
        var canvas = document.getElementById("shotCanvas");
        var ctx = canvas.getContext("2d");
        var targetBuffer = "{targetPolyBuffer}";
        var points = targetBuffer.split("@");
        var shape = new Array();        
        '''        
        scriptTarget = scriptTarget.format(targetPolyBuffer = targetPolyBuffer)
          
        # Unrolls the poly                
        scriptTarget = scriptTarget + '''                
        for (var pointIndex in points)
        {
            if (points[pointIndex] != "")
            {
                pointData = points[pointIndex].split(":");
                pointData = pointData.reverse();
                shape.push(pointData[0]);
                shape.push(pointData[1]);
            }
        }
        
        // Target outline
        ctx.beginPath();
        ctx.moveTo(shape.shift(), shape.shift());
        while(shape.length)
        {
          ctx.lineTo(shape.shift(), shape.shift());
        }
        ctx.fillStyle="#888888";
        ctx.strokeStyle="#FF0000";
        ctx.stroke()
        ctx.closePath();
        '''
        
        # Support for an image in the background
        canvasBackground = ""
        if showLastImage:
            goat = random.randint(1, 1000000)
            canvasBackground = 'background-image: url(/Images/lastPhoto.png?goat=' + str(goat) + ');'            
        
        # Allow extra script segments to be passed over
        scriptTarget = scriptTarget + extraScript
        
        
        #### The final parts
        buffer = ''
        buffer = buffer + '<div id="_mid">'
        buffer = buffer + '<div id="midCanvasDiv" style="margin: 0 auto; text-align: center; width:{canvasSizeX}px; height:{canvasSizeY}px; {canvasBackground}">'
        buffer = buffer + '<canvas id="shotCanvas" width="{canvasSizeX}" height="{canvasSizeY}" style="border:1px solid #444444;"></canvas>'
        buffer = buffer + '</div>'
        buffer = buffer + '<script>'
        buffer = buffer + '{scriptTarget}'
        buffer = buffer + '</script>'        
        buffer = buffer + '</div>'
        
        buffer = buffer.format(canvasSizeX = canvasSizeX,
                               canvasSizeY = canvasSizeY,
                               scriptTarget = scriptTarget,
                               canvasBackground = canvasBackground)
        
        return buffer