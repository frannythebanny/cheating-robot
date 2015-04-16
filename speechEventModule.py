from naoqi import ALModule
from naoqi import ALProxy

NAO_IP = "169.254.95.24" 
NAO_PORT = 9559

SpeechEventListener = None
leds = None
memory = None

class SpeechEventModule(ALModule):
    def __init__(self, name, ext_memory):
        ALModule.__init__(self, name)
        global memory
        memory = ext_memory
        memory.subscribeToEvent("ALTextToSpeech/CurrentBookMark", "SpeechEventListener", "onBookmarkDetected")
        global leds 
        leds = ALProxy("ALLeds",NAO_IP, NAO_PORT)        

    def onBookmarkDetected(self, key, value, message):
        print "Event detected!"
        print "Key: ", key
        print "Value: " , value
        print "Message: " , message

        if(value == 1):
            global leds
            leds.fadeRGB("FaceLeds", 0x00FF0000, 0.2)
        if(value == 2):
            global leds
            leds.fadeRGB("FaceLeds", 0x000000FF, 0.2)
