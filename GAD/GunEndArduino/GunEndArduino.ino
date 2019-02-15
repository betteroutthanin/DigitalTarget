
// Knock sensor related 
const int knockSensor = A0;           // the piezo is connected to analog pin 0
int       knockSensorThreshold = 50;  // threshold value to decide when the knock is detected
int       knockSensorReading = 0;     // last reading from the knock sensor

// Hold time for laser and Pi Pins
int       holdTimeMS = 500;
boolean   forceLaser = false;

// Laser Pin
const int laserPin = 11;

// RPI indicator line
const int rpiIndicatorPin = 13;

// Serial buffer bits
char buffer[10];
char currentByte = 0;
byte incomingByte = 0;

byte posOfEnd = 0;
byte posOfMid = 0;

// *****************************************************
void setup()
{
  // Clean the serial buffer  
  memset(buffer, 0, sizeof(buffer));
  currentByte = 0;  
  
  // Indicator LED
  pinMode(laserPin, OUTPUT);
  digitalWrite(laserPin, LOW);  

  // rpi Indicator
  pinMode(rpiIndicatorPin, OUTPUT);
  digitalWrite(rpiIndicatorPin, LOW);  
  
  Serial.begin(9600);
  Serial.print("Boot:Yes\n");
  // Serial.print("KT:" + String(knockSensorThreshold, DEC) + "\n");
}

// *****************************************************
void loop()
{
  knockSensorReading = analogRead(knockSensor);
  if (knockSensorReading >= knockSensorThreshold)
  {
    //tell the RPI
    digitalWrite(rpiIndicatorPin, HIGH); 

    // Turn on the idicator LED to let the user know that a detection has tacken place
    digitalWrite(laserPin, HIGH);
  
    // sleep now
    delay(holdTimeMS);

    //reset the lines
    digitalWrite(rpiIndicatorPin, LOW); 
    digitalWrite(laserPin, LOW); 
  }
  
  // Laser can be forced on
  if (forceLaser)
  {
    digitalWrite(laserPin, HIGH); 
  }
  else
  {
    digitalWrite(laserPin, LOW); 
  }
  
  if (Serial.available() > 0)
  {
    // read the incoming byte:
    incomingByte = Serial.read();
    
    if (incomingByte == '\n')
    {
        ProcessBuffer();
        // set up for next run
        currentByte = 0;
        memset(buffer, 0, sizeof(buffer));
    }
    else
    {
        buffer[currentByte++] = incomingByte;
    }
  }
}

// *****************************************************
bool CompareString(char* haystack, char* needle, byte startIndex, byte endIndex)
{
    // Assume all is good . . . until it is not
    bool outcome = true;
    for (byte i = 0; i < (endIndex - startIndex); i++)
    {
        if (haystack[startIndex + i] != needle[i])
        {
            outcome = false;
        }
    }
    return outcome;
}

// *****************************************************
void ProcessBuffer(void)
{
    // terminate the string - string termination should not be needed
    // Buffer was memset with 0    
    
    // Commands sent from the RPI look like this
    // SK:1500\0    
    // reset some key vars
    posOfEnd = 0;
    posOfMid = 0;
    
    // Look for the :, punch we can't find it
    for(byte i = 0; i < sizeof(buffer); i++)
    {
        // test for mid marker
        if (buffer[i] == ':')
        {
            posOfMid = i;
        }

        // set for end marker
        if (buffer[i] == '\0')
        {
            posOfEnd = i;
        }
    }
    
    // Validate to make sure we got valid Mid and End markers
    if (posOfMid == 0){return;}
    if (posOfEnd == 0){return;}
    if (posOfEnd == posOfMid){return;}
    
    // Ok we have some valid data
    // Time to get the gold
    
    // Set for Knock Set (KS)
    if (CompareString(buffer, "KS", 0, posOfMid) == true)
    {
        knockSensorThreshold = atoi(&buffer[posOfMid + 1]);
        Serial.print("KV:" + String(knockSensorThreshold, DEC) + "\n");        
    }
    
    // Laser timing set (TS)
    if (CompareString(buffer, "TS", 0, posOfMid) == true)
    {
        holdTimeMS = atoi(&buffer[posOfMid + 1]);
        Serial.print("TV:" + String(holdTimeMS, DEC) + "\n");        
    }
    
    // Force Laser set (LS)
    if (CompareString(buffer, "LS", 0, posOfMid) == true)
    {
        if(CompareString(buffer, "on", posOfMid+1, posOfEnd))
        {
            forceLaser = true;  
        }
        else
        {
          forceLaser = false;
        }
        
    }


    
}
