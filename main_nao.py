from naoqi import ALProxy, ALBroker
from speechEventModule import SpeechEventModule

myString = "Put that \\mrk=1\\ there."
NAO_IP = "169.254.95.24" 
NAO_IP = "10.0.1.3" 
NAO_PORT = 9559
memory = ALProxy("ALMemory", NAO_IP, NAO_PORT)
tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
tts.enableNotifications()

myBroker = ALBroker("myBroker",
   "0.0.0.0",   # listen to anyone
   0,           # find a free port and use it
   NAO_IP,         # parent broker IP
   NAO_PORT)       # parent broker port

global SpeechEventListener
SpeechEventListener = SpeechEventModule("SpeechEventListener", memory)
tts.say("Hey")
