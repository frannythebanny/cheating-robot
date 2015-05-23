import hangman
import pandas as pd
import numpy as np

import random

import motion

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser
from hangman_speechevent import SpeechEventModule

import time

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "10.0.1.3"




# Initialize text to Speech
tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
tts.enableNotifications()


def nao_speech(possible_sentences):
    """
    Let Nao randomly select one of the possible sentences and speak them out loud
    """

    tts.say("\\bound=S\\\\rspd=75\\" + random.choice(possible_sentences))


# Initialize motion
motionProxy = ALProxy("ALMotion", NAO_IP, 9559)
postureProxy = ALProxy("ALRobotPosture", NAO_IP, 9559)

# Motion further parameters
space     = motion.FRAME_ROBOT
useSensor = False
effectorName = "LArm"

effectorInit = motionProxy.getPosition(effectorName, space, useSensor)

# Active LArm tracking
isEnabled = True
motionProxy.wbEnableEffectorControl(effectorName, isEnabled)

coef = 1.0
if (effectorName == "LArm"):
    coef = +1.0
elif (effectorName == "RArm"):
    coef = -1.0

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

postureProxy.goToPosture("Stand", 0.5)

targetCoordinateList = [
[ +0.4, +0.00*coef, +0.4], # target1 for LArm
[ +0.00, +0.00*coef, +0.00], # target2 for LArm
[ +1.00, +1.00*coef, +1.00], # target2 for LArm
]

# Set NAO in Stiffness On
StiffnessOn(motionProxy)

# Give hand
for i, targetCoordinate in enumerate(targetCoordinateList):
    print(i)
    print(targetCoordinate)
    targetCoordinate = [targetCoordinate[i] + effectorInit[i] for i in range(3)]
    motionProxy.wbSetEffectorControl(effectorName, targetCoordinate)
    time.sleep(4.0)
    if i == 0:
        nao_speech(["Hi, my name is Naomi!"])
        time.sleep(4.0)

# Deactivate LArm tracking
isEnabled    = False
motionProxy.wbEnableEffectorControl(effectorName, isEnabled)