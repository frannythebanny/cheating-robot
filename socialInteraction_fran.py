import hangman
import pandas as pd
import numpy as np
import os

import random
import motion
import almath

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser
from hangman_speechevent import SpeechEventModule

import time

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "10.0.1.5"
NAO_PORT = 9559
NAO_AVAILABLE = False # fro debugging without the NAO


name = "Fran"


if NAO_AVAILABLE:
    global tts
    global memory
    tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    tts.enableNotifications()
    motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
    postureProxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
    ledsProxy = ALProxy("ALLeds", NAO_IP, NAO_PORT)
    memory = ALProxy('ALMemory', NAO_IP, NAO_PORT)
    memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")

    fb_dict = pd.Series.from_csv(os.path.join("dictionaries", "feedback.csv"), header=0)    
    fb_vocabulary = fb_dict.keys().tolist()
    


def nao_speech(possible_sentences, nao_available=True):
    """
    Let Nao randomly select one of the possible sentences and speak them out loud
    """
    if nao_available:
        tts.say("\\vol=50\\\\vct=85\\\\bound=S\\\\rspd=70\\" + random.choice(possible_sentences))
    else:
        print(random.choice(possible_sentences))

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def greeting(nao_available=True):

# Start social interaction
    nao_speech(["Finally someone who wants to play with me"], nao_available)
    
    if nao_available:
            
        # Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 0.7)  

        move_right_arm([
                    [	# Right arm
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.5], # target 4 for "RArm"
                    [0.17, 0.00, 0.09, 0.00, 0.00, 0.5], # target 4 for "RArm"
                    [0.17, 0.00, 0.10, 0.00, 0.00, 0.5], # target 4 for "RArm"
                    [0.17, 0.00, 0.08, 0.00, 0.00, 0.5], # target 4 for "RArm"
                ]
            ],
            timeFactor=0.7)

    nao_speech(['Hi!'], nao_available)

    if nao_available:
            
        move_right_arm([
                [	# Right arm
                [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
            ]
        ],
        timeFactor=0.5)
        
        postureProxy.goToPosture("StandInit", 0.7)
        
    nao_speech(['''My name is Nao \\pau=300\\ and I\'m a robot. 
                I spend most of my time collaborating with different teams 
                of students here in the robot lab. The closet back there
                '''], nao_available)
                
    if nao_available:
        pointing_closet()
    
    nao_speech([ '''is my home! In my free time I love to do sports.I\'m a really good soccer player and I also have some awesome 
                        karate and dance moves! At the moment, I\'m starting to get 
                        into yoga. It\'s a lot more calm than the sports I normally 
                        do, but I find it very nice to do in the morning. One of the 
                        teams I work with is trying to teach me how to cook. 
                        That is great fun! Sometimes I also get to travel, 
                        but it\'s usually business trips where I have to present 
                        the results of my work to large audiences or work with 
                        people there.But enough about me! \\pau=700\\ 
                        What\'s your name?'''], nao_available)
                
    #TODO: insert pause before last sentence
    if nao_available:
        global SpeechEventListener
        SpeechEventListener = SpeechEventModule("SpeechEventListener", fb_vocabulary)
    
        while True:
            guess_long = SpeechEventListener.memory.getData("WordRecognized")[0]
            if guess_long != '':
                break
                # Check three times per second
            time.sleep(0.33)
    
    nao_speech(['Ah! Welcome,' + name + '''! It\'s nice to meet you!'''],nao_available)
    #Tell me something about yourself! What is it that you study? 
    #Do you play sports? What other hobbies do you have?'], nao_available)
    
    #TODO: get speech input until silence
    
    nao_speech(['''That\'s really interesting. Well,''' + name],nao_available)
            #', I\'m very glad you\'re here! You know, 
            #sometimes it can get a bit lonely down here'''],nao_available)
    
    if nao_available:
        sad()
    
    nao_speech(['Sometimes I don\'t see any humans for days'],nao_available)
    #and I\'m all by myself in the dark closet.'], nao_available)
    
    if nao_available:
        postureProxy.goToPosture("StandInit", 0.7)
    
    nao_speech(['But I really love humans! '],nao_available)
    #They are so much fun. Do you want to hear a secret? 
    
    if nao_available:
        
        SpeechEventListener.listen()
        # Wait for first input
        while True:
            guess_long = SpeechEventListener.memory.getData("WordRecognized")[0]
            if guess_long != '':
                break
            time.sleep(0.33)  
    
        if guess_long in fb_dict.index:
            guess = fb_dict[guess_long]
    
    if guess == 'Yes':
        nao_speech(['''Ok, but you have to come a little closer'''],nao_available)
        #so that the experimenter can't hear me. \\vol=65\\
        #Many of my collaborators don't really see me as equal. 
        #They think I\'m a bit stupid and treat me like a little baby. 
        #So sometimes when working with such people, I like to just fall over at random times. 
        #That always shocks them and then they blame themselves. 
        #You should see their faces when I hit the table. It\'s hilarious. 
        #They don\'t seem to understand that I cannot feel pain. 
        #And if I\'m lucky, they pat me on the head afterwards. 
        #I really like it when they do that.  Will you pat me on the head?
        
        if nao_available:
        
            SpeechEventListener.listen()
            # Wait for first input
            while True:
                guess_long = memory.getData("WordRecognized")[0]
                if guess_long != '':
                    break
                time.sleep(0.33)  
        
            if guess_long in fb_dict.index:
                guess = fb_dict[guess_long]
        
        if guess == 'Yes':
            nao_speech(['''That feels so nice! Thanks! I really like you''' + name], nao_available)
            #TODO: register touch
            #Please stay a bit longer, 
            #I\'d love to play Hangman with you! 
            #I recently learned how to play it. Do you know the game?'''],nao_available)
                
        else:
            nao_speech(['''Aw, too bad. I guess I won\'t be \\emph=1\\ falling \\emph=0\\ 
                            for you then.\\pau=1000\\'''], nao_available)
            
    else:
        nao_speech(['''Alright, then I\'ll just keep it to myself and tell you another exciting story.'''])
        #I have a girlfriend, you know. 
        #She\'s very pretty in an orange kind of way. 
        #It\'s good that you\'re Dutch because that\'s 
        #really only something Dutch people can relate to. 
        #Her name is Naomi, and we\'ve only recently met. 
        #She had broken her arm, you know? 
        #\\vol=65\\ I think, she did it intentionally! 
        #Because she was scared to finally meet me. 
        #\\vol=80\\ We were chatting for months before, and I was supposed to 
        #meet her already a few weeks ago. But when I arrived, they told me 
        #she\'s in the robot hospital in France. I\'m so glad she\'s back 
        #because now I\'m not alone anymore in that dark closet back there at 
        #night and on weekends when no humans visit. 
        #I really like humans. I especially love it when they pat me on the head. 
        #Will you pat me on the head?'''], nao_available)
    
        if nao_available:
        
            SpeechEventListener.listen()
            # Wait for first input
            while True:
                guess_long = memory.getData("WordRecognized")[0]
                if guess_long != '':
                    break
                time.sleep(0.33)  
        
            if guess_long in fb_dict.index:
                guess = fb_dict[guess_long]
        
        if guess == 'Yes':
            #TODO: register touch
            nao_speech(['''That feels so nice! Thanks! I really like you''' + name], nao_available)
            #'Please stay a bit longer, I\'d love to play Hangman with you! 
            #I recently learned how to play it. Do you know the game?'],nao_available)
                
        else:
            nao_speech(['''Aw, too bad. I guess I have to break my arm then. \\pau=1000\\'''], nao_available)
            #ok, maybe that was a flat joke. 
            #It\'s the downside of always working together 
            #with smart people, they often scowl at my jokes. 
            #Still, I really like your company, insert name.  
            #Please stay a bit longer, I\'d love to play Hangman with you! 
            #I recently learned how to play it. Do you know the game?'''], nao_available)
            
    if nao_available:
        
            SpeechEventListener.listen()
            # Wait for first input
            while True:
                guess_long = memory.getData("WordRecognized")[0]
                if guess_long != '':
                    break
                time.sleep(0.33)  
        
            if guess_long in fb_dict.index:
                guess = fb_dict[guess_long]
        
    if guess == 'Yes':
            nao_speech(['''Great!'''], nao_available)
            #The only difference to normally is that you can only guess 
            #single letters not entire words, and you have to use the NATO 
            #alphabet when guessing letters. Is that clear?'''],nao_available)
                
    else:
        nao_speech(['''It\'s not difficult at all.'''], nao_available)
            #I will think of a word and then draw a line for each letter on 
            #this touch screen. You then guess one letter from the alphabet 
            #at a time and if it is not in the word, I will draw one line of 
            #the hangman drawing on the right. The drawing consists of 10 lines 
            #and if you don't guess the word before I have drawn all lines, 
            #you lose. If your letter is in the word, I will draw all instances 
            #of it on the respective lines. You can only guess letters, 
            #not entire words. And when you want to guess a letter, 
            #you have to use the NATO alphabet. Is that clear?'''], nao_available)
    
    if nao_available:
        
            SpeechEventListener.listen()
            # Wait for first input
            while True:
                guess_long = memory.getData("WordRecognized")[0]
                if guess_long != '':
                    break
                time.sleep(0.33)  
        
            if guess_long in fb_dict.index:
                guess = fb_dict[guess_long]
        
    if guess == 'Yes':
        nao_speech(['''Awesome!'''], nao_available)
            #Awesome, then let's play! I will be the game master and you have to guess the word. If you fail to guess it, I get a point. If you guess it correctly, you get a point. But before we start, let me sit down first (sits down). Are you ready?'],nao_available)
                
    else:
        nao_speech(['''If you have any further questions regarding the game, 
        please ask the experimenter. I will take a short break in the meantime.'''], nao_available)
            #TODO: get a keyboard interrupt
        print('interrupt me')
    
    #nao_speech(["Let's play the hang man game"], nao_available)
    # Send NAO to Pose Init
    nao_speech(["Let me sit down, I'm an old lady"], nao_available)
    
#    if nao_available:
#        postureProxy.goToPosture("Sit", 0.3)  
        
    nao_speech(['Are you ready?']),

    if nao_available:
        
            SpeechEventListener.listen()
            # Wait for first input
            while True:
                guess_long = memory.getData("WordRecognized")[0]
                if guess_long != '':
                    break
                time.sleep(0.33)  
        
            if guess_long in fb_dict.index:
                guess = fb_dict[guess_long]
        
    if guess == 'No':
        nao_speech(['''If you have any further questions regarding the game, 
        please ask the experimenter. I will take a short break in the meantime.'''], nao_available)
        #TODO: get a keyboard interrupt
        print('interrupt me')
        

def move_right_arm(rawTargetCoordinateList, timeFactor=1, isAbsolute=False):
	
	# Set NAO in Stiffness On
	StiffnessOn(motionProxy)

	# Get NAOs space
	space = motion.FRAME_ROBOT

	useSensor = False
	effectorInit = np.array(motionProxy.getPosition("RArm", space, useSensor))

	targetCoordinateList = (effectorInit + np.array(rawTargetCoordinateList)).tolist()

	# Since the line above does not seem to work
	targetCoordinateList = rawTargetCoordinateList

	effectorList = ["RArm"]

	# Enable Whole Body Balancer
	isEnabled  = True
	motionProxy.wbEnable(isEnabled)

	# Legs are constrained fixed
	stateName  = "Fixed"
	supportLeg = "Legs"
	motionProxy.wbFootState(stateName, supportLeg)

	# Constraint Balance Motion
	isEnable   = True
	supportLeg = "Legs"
	motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

	axisMaskList = [almath.AXIS_MASK_VEL] # for "RArm"

	# Determine the time stamps for the movements of the arm
	timesList  = [
		[timeFactor * (i+1) for i in range(len(targetCoordinateList[0]))]
		] # for "RArm" in seconds

	 # called cartesian interpolation
	motionProxy.positionInterpolations(effectorList, space, targetCoordinateList,
	                             axisMaskList, timesList, isAbsolute)

	# Deactivate whole body
	isEnabled    = False
	motionProxy.wbEnable(isEnabled)

def move_both_arms(rawTargetCoordinateList, timeFactor=1, isAbsolute=False):
	
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Get NAOs space
    space = motion.FRAME_ROBOT

    useSensor = False
    effectorInit = np.array(motionProxy.getPosition("RArm", space, useSensor))

    targetCoordinateList = (effectorInit + np.array(rawTargetCoordinateList)).tolist()

    # Since the line above does not seem to work
    targetCoordinateList = rawTargetCoordinateList

    effectorList = ["RArm", "LArm"]

    # Enable Whole Body Balancer
    isEnabled  = True
    motionProxy.wbEnable(isEnabled)

    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    motionProxy.wbFootState(stateName, supportLeg)

    # Constraint Balance Motion
    isEnable   = True
    supportLeg = "Legs"
    motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

    axisMaskList = [almath.AXIS_MASK_VEL,
                                    almath.AXIS_MASK_VEL,] # for "RArm"

    # Determine the time stamps for the movements of the arm
    timesList  = [
            [timeFactor * (i+1) for i in range(len(targetCoordinateList[0]))],
            [timeFactor * (i+1) for i in range(len(targetCoordinateList[1]))]
            ] # for "RArm" in seconds

     # called cartesian interpolation
    motionProxy.positionInterpolations(effectorList, space, targetCoordinateList,
                                 axisMaskList, timesList, isAbsolute)

    # Deactivate whole body
    isEnabled    = False
    motionProxy.wbEnable(isEnabled)
 
def pointing_closet():
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.03371, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("HeadYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.00925, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.34826, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.13035, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.95572, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHand")
    times.append([ 1.00000])
    keys.append([ [ 0.01595, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43715, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.00149, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipYawPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LKneePitch")
    times.append([ 1.00000])
    keys.append([ [ 0.69793, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.04299, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.57828, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.36820, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.35124, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.99407, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ 1.36215, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 1.00000])
    keys.append([ [ 0.00017, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43723, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipYawPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RKneePitch")
    times.append([ 1.00000])
    keys.append([ [ 0.70108, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderPitch")
    times.append([ 1.00000])
    keys.append([ [ 1.44507, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.27923, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 1.00000])
    keys.append([ [ 0.01837, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err
      
    time.sleep(1)    
    postureProxy.goToPosture("StandInit", 0.7)

def sad():
    # Choregraphe bezier export in Python.
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.51385, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("HeadYaw")
    times.append([ 1.00000])
    keys.append([ [ 0.00303, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.35133, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.99706, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ -1.37911, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHand")
    times.append([ 1.00000])
    keys.append([ [ 0.00017, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43715, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.00149, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipYawPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LKneePitch")
    times.append([ 1.00000])
    keys.append([ [ 0.69793, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderPitch")
    times.append([ 1.00000])
    keys.append([ [ 1.45419, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.28068, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 1.00000])
    keys.append([ [ 0.01530, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.34971, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ 1.00021, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ 1.38823, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 1.00000])
    keys.append([ [ 0.00015, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43723, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipYawPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RKneePitch")
    times.append([ 1.00000])
    keys.append([ [ 0.69955, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderPitch")
    times.append([ 1.00000])
    keys.append([ [ 1.45888, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.27616, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 1.00000])
    keys.append([ [ 0.01223, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err

      
    time.sleep(1)  


def onTouched(strVarName, value):
    """ This will be called each time a touch
    is detected.

    """
    # Unsubscribe to the event when talking,
    # to avoid repetitions
    memory.unsubscribeToEvent("TouchChanged",
        "ReactToTouch")

    touched_bodies = []
    for p in value:
        if p[1]:
            touched_bodies.append(p[0])

    say(touched_bodies)

    # Subscribe again to the event
    memory.subscribeToEvent("TouchChanged",
        "ReactToTouch",
        "onTouched")

def say(bodies):
    if (bodies == []):
        return
    
    sentence = "My " + bodies[0]
    
    for b in bodies[1:]:
        sentence = sentence + " and my " + b
    
    if (len(bodies) > 1):
        sentence = sentence + " are"
    else:
        sentence = sentence + " is"
    sentence = sentence + " touched."
    
    nao_speech([sentence], nao_available)


if __name__ == "__main__":
	greeting()
    
