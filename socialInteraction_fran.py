import hangman
import pandas as pd
import numpy as np
import os

#import pyttsx


import random
import time

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "10.0.1.5"
NAO_PORT = 9559
name = 'Fran'

# Good for debugging because then we can test it without having the nao
NAO_AVAILABLE = True
LINUX_AVAILABLE= False

if NAO_AVAILABLE:

    from optparse import OptionParser
    from hangman_speechevent import SpeechEventModule

    import motion
    import almath
    
    from naoqi import ALProxy
    from naoqi import ALBroker
    from naoqi import ALModule
    
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
    elif LINUX_AVAILABLE:
        engine = pyttsx.init()
        engine.say(random.choice(possible_sentences))
        engine.runAndWait()
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
            
        handshake()
        
    else:
        print('ACTION: nao moves her arm to do handshake')

    nao_speech(['Hi!'], nao_available)

    if nao_available:
        
        for i in range(1,4):     
            move_arm_up()
            move_arm_down()
        
        postureProxy.goToPosture("StandInit", 0.7)
    else:
        print('ACTION: nao moves arm up and down four times')
        
    nao_speech(['''My name is Naomi \\pau=300\\ and I\'m a robot. 
                The closet back there
                '''], nao_available)
    
    #TODO: perhaps coordinate this with speech through animated speech            
    if nao_available:
        pointing_closet()
    else: 
        print('ACTION: nao points to closet')
    
    nao_speech([ '''is my home! In my free time I love to do sports.I\'m a 
    really good soccer player and I also have some awesome\\pau=300\\ 
    karate and dance moves! At the moment, I\'m starting to get into yoga. 
    It\'s a lot more calm than the sports I normally do, but very nice 
    in the morning. But enough about me! \\pau=700\\ What\'s your name?'''], nao_available)
                
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
    else:
        # Text input
        guess_long = raw_input("DEBUG: Please enter your name:   ")
    
    nao_speech(['Ah! Welcome, ' + name + ''' ! It\'s nice to meet you!
            I\'m very glad you\'re here! You know, 
            sometimes it can get a bit lonely down here'''],nao_available)
            
    if nao_available:
        sad()
    else: 
        print('ACTION: nao bows her head to look sad')
    
    nao_speech(['''Sometimes I don\'t see any humans for days
    and I\'m all by myself in the dark closet. But I really love humans!'''], nao_available)
    
    if nao_available:
        postureProxy.goToPosture("StandInit", 0.7)
        
    nao_speech(['They are so much fun. \\pau=700\\ Do you want to hear a secret?'],nao_available)
    
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
            
    else:
        # Text input
        guess = raw_input("DEBUG: Yes/No?:   ")
    
    if guess == 'Yes':
        nao_speech(['''Ok, but you have to come a little closer.\\vol=65\\
        Sometimes when working with students, I like to just fall over at random times. 
        \\pau=500\\ Haha! \\pau=300\\ You should see their faces when I hit the table. 
        It\'s hilarious.\\pau=1000\\ Oh! I really like you ''' + name +
        ''' Please stay a bit longer, I\'d love to play Hangman with you! 
        I recently learned how to play it. Do you know the game?'''],nao_available)
            
    else:
        nao_speech(['''Alright, then I\'ll just keep it to myself and 
        tell you something else. \\pau=700\\ I recently got a boyfriend.
        His name is Yob. He's just great! He is even learning how to cook, just for me! 
        I\'m so glad he\'s here, because now I\'m not alone anymore in that dark closet back there at 
        night and on weekends when no humans visit. I really like humans. I really like you ''' + name +
        ''' Please stay a bit longer, I\'d love to play Hangman with you! 
        I recently learned how to play it. Do you know the game?'''],nao_available)
            
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
    else:
        # Text input
        guess = raw_input("DEBUG: Yes/No?:   ")        
        
    if guess == 'Yes':
            nao_speech(['''Great! The only difference to normally is that you can only guess 
            single letters not entire words, and you have to use the NATO 
            alphabet when guessing letters. Your guesses and the hangman are 
            displayed on this touch screen.'''], nao_available)  
            if nao_available:
                pointing_to_phone()    
            else: 
                print('ACTION: nao points to phone')
            nao_speech(['Is that clear?'],nao_available)              
    else:
        nao_speech(['''It\'s not difficult at all.
        I will think of a word and then draw a line for each letter on 
        this touch screen.'''], nao_available)
        if nao_available:
            pointing_to_phone()    
        else: 
            print('ACTION: nao points to phone')
        nao_speech(['''You then guess one letter from the alphabet 
        at a time and if it is not in the word, I will draw one line of 
        the hangman drawing on the right. The drawing consists of 10 lines 
        and if you don't guess the word before I have drawn all lines, 
        you lose. If your letter is in the word, I will draw all instances 
        of it on the respective lines. You can only guess letters, 
        not entire words. And when you want to guess a letter, 
        you have to use the NATO alphabet. Is that clear?'''], nao_available)
    
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
    else:
        # Text input
        guess = raw_input("DEBUG: Yes/No?:   ")
        
    if guess == 'Yes':
        nao_speech(['''Awesome, then let's play! I will be the game master 
        and you have to guess the word. If you fail to guess it, I get a point. 
        If you guess it correctly, you get a point. But before we start, 
        let me sit down first, I'm an old lady.'''], nao_available)
        if nao_available:
            postureProxy.goToPosture("Sit", 0.7)
        else: 
            print('Nao sits down')
                
    else:
        nao_speech(['''If you have any further questions regarding the game, 
        please ask the experimenter. I will take a short break in the meantime.'''], nao_available)
        if nao_available:
            postureProxy.goToPosture("Sit", 0.7)
        else: 
            print('Nao sits down')
        raw_input("Press Enter to continue   ")
        
        
    nao_speech(['Alright, \\pau=500\\ are you ready?'], nao_available),

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
    else:
        guess = raw_input('DEBUG: Yes/No?:   ')
        
    if guess == 'No':
        nao_speech(['''If you have any further questions regarding the game, 
        please ask the experimenter. I will take a short break in the meantime.'''], nao_available)
        raw_input("Press Enter to continue   ")

if __name__ == "__main__":
	greeting()

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
      motion = ALProxy("ALMotion", IP, 9559)
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

def handshake():
    # Choregraphe bezier export in Python.
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.02143, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("HeadYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.00925, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.34979, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.99706, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ -1.38064, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
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
    keys.append([ [ 1.42965, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.28988, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.00311, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.34971, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.76091, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ 1.66281, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 1.00000])
    keys.append([ [ 0.01650, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43877, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
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
    keys.append([ [ 0.66120, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.23619, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.07214, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err

def move_arm_up():
        # Choregraphe bezier export in Python.
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.02143, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
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
    keys.append([ [ -0.98632, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ -1.37911, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHand")
    times.append([ 1.00000])
    keys.append([ [ 0.00019, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43868, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.00149, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipYawPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LKneePitch")
    times.append([ 1.00000])
    keys.append([ [ 0.69946, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderPitch")
    times.append([ 1.00000])
    keys.append([ [ 1.43425, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.28988, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.00311, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.34971, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.91737, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ 1.64747, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 1.00000])
    keys.append([ [ 0.01650, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43877, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
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
    keys.append([ [ 0.43263, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.26687, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 1.00000])
    keys.append([ [ 0.08433, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err

def move_arm_down():
        # Choregraphe bezier export in Python.
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.02143, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
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
    keys.append([ [ -0.97558, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ -1.37911, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHand")
    times.append([ 1.00000])
    keys.append([ [ 0.00021, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43868, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.00149, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipYawPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LKneePitch")
    times.append([ 1.00000])
    keys.append([ [ 0.69946, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderPitch")
    times.append([ 1.00000])
    keys.append([ [ 1.43425, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.28988, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.00311, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.34971, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.94652, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ 1.56464, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 1.00000])
    keys.append([ [ 0.01650, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43877, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
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
    keys.append([ [ 0.98640, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.22699, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.01998, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err

def pointing_to_phone():
        # Choregraphe bezier export in Python.
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.02297, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("HeadYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.00925, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.35286, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.97558, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ -1.37911, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHand")
    times.append([ 1.00000])
    keys.append([ [ 0.00021, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipPitch")
    times.append([ 1.00000])
    keys.append([ [ -0.43868, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.00149, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipYawPitch")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LKneePitch")
    times.append([ 1.00000])
    keys.append([ [ 0.69946, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderPitch")
    times.append([ 1.00000])
    keys.append([ [ 1.43425, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.28988, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 1.00000])
    keys.append([ [ -0.00311, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 1.00000])
    keys.append([ [ -0.34971, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 1.00000])
    keys.append([ [ 0.11663, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 1.00000])
    keys.append([ [ 1.65054, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 1.00000])
    keys.append([ [ 0.01650, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
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
    keys.append([ [ 0.93271, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 1.00000])
    keys.append([ [ -0.54461, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 1.00000])
    keys.append([ [ 0.10887, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err

def wave():
	# Choregraphe bezier export in Python.
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([ 0.80000, 1.56000, 2.24000, 2.80000, 3.48000, 4.60000])
	keys.append([ [ 0.29602, [ 3, -0.26667, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.17032, [ 3, -0.25333, 0.11200], [ 3, 0.22667, -0.10021]], [ -0.34059, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ -0.05987, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ -0.19333, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ -0.01078, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("HeadYaw")
	times.append([ 0.80000, 1.56000, 2.24000, 2.80000, 3.48000, 4.60000])
	keys.append([ [ -0.13503, [ 3, -0.26667, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.35133, [ 3, -0.25333, 0.04939], [ 3, 0.22667, -0.04419]], [ -0.41576, [ 3, -0.22667, 0.00372], [ 3, 0.18667, -0.00307]], [ -0.41882, [ 3, -0.18667, 0.00307], [ 3, 0.22667, -0.00372]], [ -0.52007, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ -0.37587, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowRoll")
	times.append([ 0.72000, 1.48000, 2.16000, 2.72000, 3.40000, 4.52000])
	keys.append([ [ -1.37902, [ 3, -0.24000, 0.00000], [ 3, 0.25333, 0.00000]], [ -1.29005, [ 3, -0.25333, -0.03454], [ 3, 0.22667, 0.03091]], [ -1.18267, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ -1.24863, [ 3, -0.18667, 0.02055], [ 3, 0.22667, -0.02496]], [ -1.31920, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ -1.18421, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowYaw")
	times.append([ 0.72000, 1.48000, 2.16000, 2.72000, 3.40000, 4.52000])
	keys.append([ [ -0.80386, [ 3, -0.24000, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.69188, [ 3, -0.25333, -0.01372], [ 3, 0.22667, 0.01227]], [ -0.67960, [ 3, -0.22667, -0.01227], [ 3, 0.18667, 0.01011]], [ -0.61057, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ -0.75324, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ -0.67040, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHand")
	times.append([ 1.48000, 4.52000])
	keys.append([ [ 0.00416, [ 3, -0.49333, 0.00000], [ 3, 1.01333, 0.00000]], [ 0.00419, [ 3, -1.01333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderPitch")
	times.append([ 0.72000, 1.48000, 2.16000, 2.72000, 3.40000, 4.52000])
	keys.append([ [ 1.11824, [ 3, -0.24000, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.92803, [ 3, -0.25333, 0.00000], [ 3, 0.22667, 0.00000]], [ 0.94030, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ 0.86207, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ 0.89735, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ 0.84212, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderRoll")
	times.append([ 0.72000, 1.48000, 2.16000, 2.72000, 3.40000, 4.52000])
	keys.append([ [ 0.36352, [ 3, -0.24000, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.22699, [ 3, -0.25333, 0.02572], [ 3, 0.22667, -0.02301]], [ 0.20398, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ 0.21779, [ 3, -0.18667, -0.00670], [ 3, 0.22667, 0.00813]], [ 0.24847, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ 0.22699, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LWristYaw")
	times.append([ 1.48000, 4.52000])
	keys.append([ [ 0.14722, [ 3, -0.49333, 0.00000], [ 3, 1.01333, 0.00000]], [ 0.11961, [ 3, -1.01333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowRoll")
	times.append([ 0.64000, 1.40000, 1.68000, 2.08000, 2.40000, 2.64000, 3.04000, 3.32000, 3.72000, 4.44000])
	keys.append([ [ 1.38524, [ 3, -0.21333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.24241, [ 3, -0.25333, 0.00000], [ 3, 0.09333, 0.00000]], [ 0.34907, [ 3, -0.09333, -0.09496], [ 3, 0.13333, 0.13565]], [ 0.93425, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.68068, [ 3, -0.10667, 0.14138], [ 3, 0.08000, -0.10604]], [ 0.19199, [ 3, -0.08000, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.26180, [ 3, -0.13333, -0.06981], [ 3, 0.09333, 0.04887]], [ 0.70722, [ 3, -0.09333, -0.10397], [ 3, 0.13333, 0.14852]], [ 1.01927, [ 3, -0.13333, -0.06647], [ 3, 0.24000, 0.11965]], [ 1.26559, [ 3, -0.24000, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowYaw")
	times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 3.72000, 4.44000])
	keys.append([ [ -0.31298, [ 3, -0.21333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.56447, [ 3, -0.25333, 0.00000], [ 3, 0.22667, 0.00000]], [ 0.39113, [ 3, -0.22667, 0.03954], [ 3, 0.18667, -0.03256]], [ 0.34818, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ 0.38192, [ 3, -0.22667, -0.03375], [ 3, 0.13333, 0.01985]], [ 0.97738, [ 3, -0.13333, 0.00000], [ 3, 0.24000, 0.00000]], [ 0.82678, [ 3, -0.24000, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHand")
	times.append([ 1.40000, 3.32000, 4.44000])
	keys.append([ [ 0.01490, [ 3, -0.46667, 0.00000], [ 3, 0.64000, 0.00000]], [ 0.01492, [ 3, -0.64000, 0.00000], [ 3, 0.37333, 0.00000]], [ 0.00742, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderPitch")
	times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 4.44000])
	keys.append([ [ 0.24702, [ 3, -0.21333, 0.00000], [ 3, 0.25333, 0.00000]], [ -1.17193, [ 3, -0.25333, 0.00000], [ 3, 0.22667, 0.00000]], [ -1.08910, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ -1.26091, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ -1.14892, [ 3, -0.22667, -0.11198], [ 3, 0.37333, 0.18444]], [ 1.02015, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderRoll")
	times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 4.44000])
	keys.append([ [ -0.24241, [ 3, -0.21333, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.95419, [ 3, -0.25333, 0.00000], [ 3, 0.22667, 0.00000]], [ -0.46024, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ -0.96033, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ -0.32832, [ 3, -0.22667, -0.04750], [ 3, 0.37333, 0.07823]], [ -0.25008, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RWristYaw")
	times.append([ 1.40000, 3.32000, 4.44000])
	keys.append([ [ -0.31298, [ 3, -0.46667, 0.00000], [ 3, 0.64000, 0.00000]], [ -0.30377, [ 3, -0.64000, -0.00920], [ 3, 0.37333, 0.00537]], [ 0.18250, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	try:
	  motionProxy.angleInterpolationBezier(names, times, keys);
	except BaseException, err:
	  print err

	postureProxy.goToPosture("Sit", 1)  


def winner_move():
	# Choregraphe bezier export in Python.
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.03839, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.03686, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.03686, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.03839, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("HeadYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.05987, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.05833, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.05833, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.05833, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LAnklePitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.92189, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.92189, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.92189, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.92258, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LAnkleRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.00004, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.00004, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.00004, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.04598, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.05518, [ 3, -0.13333, 0.00920], [ 3, 0.10667, -0.00736]], [ -0.12114, [ 3, -0.10667, 0.01227], [ 3, 0.50667, -0.05829]], [ -0.26687, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.78392, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.78852, [ 3, -0.13333, 0.00460], [ 3, 0.10667, -0.00368]], [ -0.94959, [ 3, -0.10667, 0.00097], [ 3, 0.50667, -0.00460]], [ -0.95419, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHand")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.01680, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.01681, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.01681, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.01682, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -1.59992, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -1.53589, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -1.53589, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -1.53589, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.24088, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.24088, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.24088, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.24088, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipYawPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.56907, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.56907, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.57061, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.57061, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LKneePitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 1.10137, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 1.10290, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 1.10290, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 1.10290, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.59515, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.13342, [ 3, -0.13333, 0.35367], [ 3, 0.10667, -0.28294]], [ -1.31468, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.59975, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.01683, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.26994, [ 3, -0.13333, -0.16704], [ 3, 0.10667, 0.13363]], [ 0.91882, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.09362, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LWristYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.62890, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.65958, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.51385, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.84212, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RAnklePitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.92198, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.92351, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.92351, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.92198, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RAnkleRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.00004, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.00004, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.00004, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.28843, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.28843, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.22247, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.72562, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.98018, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.98939, [ 3, -0.13333, -0.00920], [ 3, 0.10667, 0.00736]], [ 1.05382, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.84519, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHand")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.01682, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.01683, [ 3, -0.13333, -0.00000], [ 3, 0.10667, 0.00000]], [ 0.01685, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.01685, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -1.53251, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -1.53097, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -1.53404, [ 3, -0.10667, 0.00027], [ 3, 0.50667, -0.00127]], [ -1.53558, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.18250, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.18250, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.18250, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.18250, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipYawPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.56907, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.56907, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.57061, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.57061, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RKneePitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 1.03396, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 1.03549, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 1.03549, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 1.03549, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.67193, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.17952, [ 3, -0.13333, 0.34231], [ 3, 0.10667, -0.27385]], [ -1.17654, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.83914, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.11356, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.49246, [ 3, -0.13333, 0.15028], [ 3, 0.10667, -0.12022]], [ -0.92504, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.19639, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RWristYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -1.20423, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -1.20423, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.82840, [ 3, -0.10667, -0.00388], [ 3, 0.50667, 0.01841]], [ -0.80999, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	try:
	  motionProxy.angleInterpolationBezier(names, times, keys);
	except BaseException, err:
	  print err

	postureProxy.goToPosture("Sit", 1)  	


def loser_move():
 # Choregraphe bezier export in Python.
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([ 1.00000])
	keys.append([ [ 0.51385, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("HeadYaw")
	times.append([ 1.00000])
	keys.append([ [ -0.14424, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LAnklePitch")
	times.append([ 1.00000])
	keys.append([ [ 0.92258, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LAnkleRoll")
	times.append([ 1.00000])
	keys.append([ [ -0.02297, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowRoll")
	times.append([ 1.00000])
	keys.append([ [ -0.51231, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowYaw")
	times.append([ 1.00000])
	keys.append([ [ -0.00618, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHand")
	times.append([ 1.00000])
	keys.append([ [ 0.01680, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipPitch")
	times.append([ 1.00000])
	keys.append([ [ -1.55237, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipRoll")
	times.append([ 1.00000])
	keys.append([ [ 0.05527, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipYawPitch")
	times.append([ 1.00000])
	keys.append([ [ -1.02314, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LKneePitch")
	times.append([ 1.00000])
	keys.append([ [ 0.49391, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderPitch")
	times.append([ 1.00000])
	keys.append([ [ 0.48317, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderRoll")
	times.append([ 1.00000])
	keys.append([ [ 0.26994, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LWristYaw")
	times.append([ 1.00000])
	keys.append([ [ -0.51700, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RAnklePitch")
	times.append([ 1.00000])
	keys.append([ [ 0.92198, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RAnkleRoll")
	times.append([ 1.00000])
	keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowRoll")
	times.append([ 1.00000])
	keys.append([ [ 0.53694, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowYaw")
	times.append([ 1.00000])
	keys.append([ [ -0.46791, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHand")
	times.append([ 1.00000])
	keys.append([ [ 0.01681, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipPitch")
	times.append([ 1.00000])
	keys.append([ [ -1.54785, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipRoll")
	times.append([ 1.00000])
	keys.append([ [ -0.13648, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipYawPitch")
	times.append([ 1.00000])
	keys.append([ [ -1.02314, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RKneePitch")
	times.append([ 1.00000])
	keys.append([ [ 0.40042, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderPitch")
	times.append([ 1.00000])
	keys.append([ [ 0.48172, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderRoll")
	times.append([ 1.00000])
	keys.append([ [ -0.09208, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RWristYaw")
	times.append([ 1.00000])
	keys.append([ [ 0.13648, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	try:
		motionProxy.angleInterpolationBezier(names, times, keys);
	except BaseException, err:
		print err

	time.sleep(1)
	postureProxy.goToPosture("Sit", 1)         
