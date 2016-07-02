from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "192.168.0.104" 
def abort_speechinput():
    asr = ALProxy("ALSpeechRecognition", NAO_IP, 9559)
    asr.subscribe("Test_ASR")
    asr.unsubscribe("Test_ASR")
    memory = ALProxy('ALMemory', NAO_IP, 9559)
    memory.unsubscribeToEvent("WordRecognized", "SpeechEventListener")
