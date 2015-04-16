from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "169.254.95.24"

class SpeechEventModule(ALModule):
    def __init__(self, name, vocabulary):
        ALModule.__init__(self, name)

        global asr
        global memory

        self.module_name = name

        asr = ALProxy("ALSpeechRecognition", NAO_IP, 9559)    
        asr.setLanguage("English")

        asr.setVocabulary(vocabulary, False)

        memory = ALProxy('ALMemory', NAO_IP, 9559)
        memory.subscribeToEvent("WordRecognized", name, "onWordRecognized")

    def onWordRecognized(self, key, value, message):
        """ does this and that """

        print "Event detected!"
        print "Key: ", key
        print "Value: " , value
        print "Message: " , message
        memory.unsubscribeToEvent("WordRecognized", self.module_name, "onWordRecognized")