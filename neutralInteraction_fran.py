import hangman
import pandas as pd
import numpy as np
import os

from global_settings import *

import send_request

import random
import time

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "10.0.1.5"
NAO_PORT = 9559
name = 'Participant'

# Good for debugging because then we can test it without having the nao

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

    fb_dict = pd.Series.from_csv(os.path.join("dictionaries", "feedback.csv"), header=0)    
    fb_vocabulary = fb_dict.keys().tolist()
    

def nao_speech(possible_sentences, nao_available=True):
    """
    Let Nao randomly select one of the possible sentences and speak them out loud
    """

    text = random.choice(possible_sentences)
    
    if nao_available:
        tts.say("\\vol=50\\\\vct=85\\\\bound=S\\\\rspd=75\\" + text)
    elif LINUX_AVAILABLE:
        engine = pyttsx.init()
        engine.setProperty("rate", 135)
        engine.say(text)
        engine.runAndWait()

    else:
        print(text)

        
def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def greeting(nao_available=True):


    # Update name of player with info from server

    settings = send_request.get_settings()
    name = str(settings['participant_name'])
    print("name is", name)
    
    # Start social interaction
    nao_speech(["Finally someone to play Hangman \\pau=300\\ with. \\pau=700\\ Do you know the game?"], nao_available)
    
    global SpeechEventListener
    SpeechEventListener = SpeechEventModule("SpeechEventListener", fb_vocabulary)
    
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
        
        nao_speech([ '''Ok, then I will just tell you some background information.\\pau=300\\
        It is not actually known where the Hangman game came from. One of the first times it is mentioned,
        is in a book from 1894. \\pau=700\\ 
        In the 19th century, criminals that committed the ultimate crime were often punished 
        with the ultimate punishment. \\pau=1000\\ Death. \\pau=700\\ 
        A hangman is the person who hangs other people. Hangmen were not very
        popular people. They were often not allowed to attend social events or even
        just enter public buildings.\\pau=700\\ 
        Hangings were public events at the time. The more infamous criminals would
        often draw many spectators. Due to this high level of entertainment, it took 
        quite some time before the practice was abolished. The last public hanging
        in Britain took place in 1964. \\pau=1000\\
        Different variants of the game exist. In some variants the gallow is 
        drawn before the game starts. In others, \\pau=700\\ the gallow is included
        in the game.\\pau=500\\ The game we will play is also a variation. 
        You may only guess single letters not entire words, and you have to use the NATO 
        alphabet when guessing letters. Your guesses and the hangman are 
        displayed on the screen. \\pau=500\\ Is that clear?'''], nao_available)
        
    else:
        nao_speech(['''Ok, then I will just tell you some background information.\\pau=300\\
        It is not actually known where the Hangman game came from. One of the first times it is mentioned,
        is in a book from 1894. \\pau=700\\ 
        In the 19th century, criminals that committed the ultimate crime were often punished 
        with the ultimate punishment. \\pau=1000\\ Death. \\pau=700\\ 
        A hangman is the person who hangs other people. Hangmen were not very
        popular people. They were often not allowed to attend social events or even
        just enter public buildings.\\pau=700\\
        The purpose of the game is to guess a word by inserting letters into blank spaces. 
        You can always only guess one letter at a time and if it is in the word, all instances are drawn.
        For each incorrect guess a line of a hangman drawing is drawn. 
        When the Hangman drawing is complete, you lose.\\pau=500\\ 
        If you guess all the letters before the drawing is finished, you win.\\pau=500\\
        Different variants of the game exist. In some variants the gallow is 
        drawn before the game starts. In others, \\pau=700\\ the gallow is included
        in the game.\\pau=500\\ The game we will play is also a variation. 
        You can only guess letters, not entire words. And when you want to guess a letter, 
        you have to use the NATO alphabet.  Your guesses and the hangman are 
        displayed on the screen. \\pau=500\\ Is that clear?'''])
    
            
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
        nao_speech(['''Ok! I will be the game master 
        and you have to guess the word. If you fail to guess it, I get a point. 
        If you guess it correctly, you get a point. But before we start, 
        let me sit down first.'''], nao_available)
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
        

if __name__ == "__main__":
	greeting()
