from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "192.168.0.104" 

class SpeechEventModule(ALModule):
    def __init__(self, name, vocabulary, wordspotting=False):
        ALModule.__init__(self, name)

        global memory
        
        self.memory = ALProxy('ALMemory', NAO_IP, 9559)
        self.module_name = name
        self.asr = ALProxy("ALSpeechRecognition", NAO_IP, 9559)
        #self.asr.setLanguage("Dutch")
        self.asr.setVocabulary(vocabulary,wordspotting)
            
#==============================================================================
#         try:
#             
#         except:
#             print("something went wrong with setting the vocabulary.")
#             pass
#==============================================================================
        
        self.listen()
        
    def listen(self):
        try:
            self.memory.unsubscribeToEvent("WordRecognized", self.module_name)
        except:
            pass
        self.memory.subscribeToEvent("WordRecognized", self.module_name, "onWordRecognized")
    
    def unsubscribeFromMemory(self):
        
        try:
            self.memory.unsubscribeToEvent("WordRecognized", self.module_name)
        except:
            pass

    def onWordRecognized(self, key, value, message):
        """ does this and that """

        print "Event detected!"
        print "Key: ", key
        print "Value: " , value
        print "Message: " , message
        if (value[0] == 'Bitterballen') & (value[1] < 0.4):
            print("I'm not confident enough that I really heard Bitterballen")
        else:
            self.memory.unsubscribeToEvent("WordRecognized", self.module_name)