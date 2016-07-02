import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse

#import socialInteraction_fran

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "192.168.0.104" 

not_touched = True

def setNot_touched(value):
    global not_touched
    not_touched=value
            
def getNot_touched():
    return not_touched


class ReactToTouch(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)

        global not_touched
        setNot_touched(True)
        # Subscribe to TouchChanged event:
        global memory
        self.memory = ALProxy("ALMemory", NAO_IP, 9559)
        self.memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")
        print("I initialize and this works")

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        touched_bodies = []
        for p in value:
            if p[1]:
                touched_bodies.append(p[0])
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        if len(touched_bodies)>=1:
            print("I registered a touch event")
            setNot_touched(False)
            memory.unsubscribeToEvent("TouchChanged",
                "ReactToTouch")
            
            

