import Config
from Ajax.Ajax import Ajax
import time

class Ajax_test(Ajax):
    ##############################################################
    def __init__(self):
        Ajax.__init__(self)
        self.loggingPrefix = "Ajax_urnData"
        
    def Process(self, requestHandler):                                
            
        #contents = 'console.log("Hello")'
        contents = '''
<canvas id="myCanvas" width="200" height="200"></canvas>

<script>
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    ctx.beginPath();
    ctx.arc(95, 50, 40, 0, 2 * Math.PI);
    ctx.stroke();
</script>

'''
        requestHandler.SendSimplePage(contents)  
        