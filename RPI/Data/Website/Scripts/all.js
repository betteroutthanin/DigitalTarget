// -----------------------------------------------------------------------------------------------------
function makeid()
{
    var text = "DataString=";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

// -----------------------------------------------------------------------------------------------------
function WebButton(Name)
{
	var xmlHttp = getXMLHttp();
	
	xmlHttp.onreadystatechange = function()
	{
		if(xmlHttp.readyState == 4)
		{			
		}
	}

	Command = "ButtonName="+Name;
	xmlHttp.open("GET", "Ajax_Button.pax"+"?"+Command, true); 
	xmlHttp.send(null);
}


// -----------------------------------------------------------------------------------------------------
function RequestStatus(Command)
{    
	var xmlHttp = getXMLHttp();
	
	xmlHttp.timeout = 1000

	xmlHttp.onreadystatechange = function()
	{
		if(xmlHttp.readyState == 4)
		{
			RequestStatus_HandleResponse(xmlHttp.responseText);
		}
	}
	
	xmlHttp.ontimeout = function()
	{

	}

	var DataString = makeid();

	xmlHttp.open("GET", Command, true);  
	xmlHttp.send(null);
}

// -----------------------------------------------------------------------------------------------------
function RequestStatus_HandleResponse(response)
{
    if (response != "")
    {        
        //console.log(response)        
        
        var menuDiv = document.getElementById('menu');
        var topDiv = document.getElementById('top');
        var midDiv = document.getElementById('mid');
        var botDiv = document.getElementById('bot');        
        var workingDiv = document.getElementById('workingSpace');
        var lastIDDiv = document.getElementById('lastID');
        
        
        // Bring over the response into the workingDiv
        workingDiv.innerHTML = response;
        
        // Update the last ID
        if (document.getElementById('_lastID'))
        {
            lastIDDiv.innerHTML = document.getElementById('_lastID').innerHTML;
        }        
        
        // Menu section
        if (document.getElementById('_menu'))
        {
            menuDiv.innerHTML = document.getElementById('_menu').innerHTML
        }
        
        // Top section
        if (document.getElementById('_top'))
        {
            topDiv.innerHTML = document.getElementById('_top').innerHTML
        }
        
        // Mid
        if (document.getElementById('_mid'))
        {
            midDiv.innerHTML = document.getElementById('_mid').innerHTML
        }
        
        // Bot
        if (document.getElementById('_bot'))
        {
            botDiv.innerHTML = document.getElementById('_bot').innerHTML
        }
        
        // test for any scripts that may need to run
        script = workingDiv.getElementsByTagName('script')[0]
        if (script)
        {            
            eval(script.text)
        }
        
        // Clean up time
        workingDiv.innerHTML = ""
        
        console.log("All done")
    }
    else
    {

    }
}

// -----------------------------------------------------------------------------------------------------
function getXMLHttp()
{
	var xmlHttp

	try
	{
		//Firefox, Opera 8.0+, Safari
		xmlHttp = new XMLHttpRequest();
	}
	catch(e)
	{
		//Internet Explorer
		try
		{
			xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
		}
		catch(e)
		{
			try
			{
				xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
			}
			catch(e)
			{
				alert("Your browser does not support AJAX!")
				return false;
			}
		}
	}
	return xmlHttp;
}