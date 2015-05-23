from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "10.0.1.3"

class SpeechEventModule(ALModule):
    def __init__(self, name, vocabulary):
        ALModule.__init__(self, name)

        global memory
        memory = ALProxy('ALMemory', NAO_IP, 9559)

        self.module_name = name

        self.asr = ALProxy("ALSpeechRecognition", NAO_IP, 9559)
            
        try:
            self.asr.setLanguage("English")
            self.asr.setVocabulary(vocabulary, False)
        except Exception, e:
            pass

        memory.subscribeToEvent("WordRecognized", self.module_name, "onWordRecognized")

    def onWordRecognized(self, key, value, message):
        """ does this and that """

        print "Event detected!"
        print "Key: ", key
        print "Value: " , value
        print "Message: " , message
        memory.unsubscribeToEvent("WordRecognized", self.module_name)