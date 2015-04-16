from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

NAO_IP = "169.254.95.24"


asr = ALProxy("ALSpeechRecognition", NAO_IP, 9559)
asr.subscribe("Test_ASR")
asr.unsubscribe("Test_ASR")
