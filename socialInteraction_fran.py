import hangman
import pandas as pd
import numpy as np
import os

import pyttsx

import send_request

import random
import time

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "10.0.1.5"
NAO_PORT = 9559
name = 'Fran'

# Good for debugging because then we can test it without having the nao
NAO_AVAILABLE = False
LINUX_AVAILABLE= True

if NAO_AVAILABLE:

    from optparse import OptionParser
    from hangman_speechevent import SpeechEventModule

    import motion
    import almath
    import nao_moves
    
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

    text = random.choice(possible_sentences)
    
    if nao_available:
        tts.say("\\vol=50\\\\vct=85\\\\bound=S\\\\rspd=70\\" + text)
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
    name = settings['participant_name']
    
    # Start social interaction
    nao_speech(["Finally someone who wants to play with me"], nao_available)
    
    if nao_available:
            
        nao_moves.handshake()
        
    else:
        print('ACTION: nao moves her arm to do handshake')

    nao_speech(['Hi!'], nao_available)

    if nao_available:
        
        for i in range(1,4):     
            nao_moves.move_arm_up()
            nao_moves.move_arm_down()
        
        postureProxy.goToPosture("StandInit", 0.7)
    else:
        print('ACTION: nao moves arm up and down four times')
        
    nao_speech(['''My name is Naomi \\pau=300\\ and I\'m a robot. 
                The closet back there
                '''], nao_available)
    
    #TODO: perhaps coordinate this with speech through animated speech            
    if nao_available:
        nao_moves.pointing_closet()
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
        raw_input("DEBUG: Please enter your name:   ")
    
    nao_speech(['Ah! Welcome, ' + name + ''' ! It\'s nice to meet you!
    Tell me something about yourself! What is it that you study? 
    Do you play sports? What other hobbies do you have?'''],nao_available)
       
    #TODO: get speech input until silence
    
    nao_speech(['That\'s really interesting.\\pau=500\\ Well, ' + name
            + ''' , I\'m very glad you\'re here! You know, 
            sometimes it can get a bit lonely down here'''],nao_available)
            
    if nao_available:
        nao_moves.sad()
    else: 
        print('ACTION: nao bows her head to look sad')
    
    nao_speech(['''Sometimes I don\'t see any humans for days
    and I\'m all by myself in the dark closet. But I really love humans!'''], nao_available)
    
    if nao_available:
        postureProxy.goToPosture("StandInit", 0.7)
        
    nao_speech(['They are so much fun. \\pau=700\\ Do you want to hear a secret?'], nao_available)
    
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
        It\'s hilarious. And if I\'m lucky, they pat me on the head afterwards. 
        I really like it when they do that.\\pau=500\\ Will you pat me on the head?'''],nao_available)
            
    else:
        nao_speech(['''Alright, then I\'ll just keep it to myself and 
        tell you something else. \\pau=700\\ I recently got a boyfriend.
        His name is Yob. He's just great! He is even learning how to cook, just for me! 
        I\'m so glad he\'s here, because now I\'m not alone anymore in that dark closet back there at 
        night and on weekends when no humans visit. I really like humans. 
        I especially love it when they pat me on the head. Will you pat me on the head?'''], nao_available)
    
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
        time.sleep(3)
        #TODO: register touch
        nao_speech(['That feels so nice! Thanks! I really like you ' + name +
        ''' Please stay a bit longer, I\'d love to play Hangman with you! 
        I recently learned how to play it. Do you know the game?'''],nao_available)
            
    else:
        nao_speech(['Aw, too bad. \\pau=1000\\ Still, I really like your company ' + name +  
        ''' Please stay a bit longer, I\'d love to play Hangman with you! 
        I recently learned how to play it. Do you know the game?'''], nao_available)
            
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
                nao_moves.pointing_to_phone()    
            else: 
                print('ACTION: nao points to phone')
            nao_speech(['Is that clear?'],nao_available)              
    else:
        nao_speech(['''It\'s not difficult at all.
        I will think of a word and then draw a line for each letter on 
        this touch screen.'''], nao_available)
        if nao_available:
            nao_moves.pointing_to_phone()    
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
        nao_speech(['Are you ready?'],nao_available)
                
    else:
        nao_speech(['''If you have any further questions regarding the game, 
        please ask the experimenter. I will take a short break in the meantime.'''], nao_available)
        if nao_available:
            postureProxy.goToPosture("Sit", 0.7)
        else: 
            print('Nao sits down')
        stop_key = raw_input("Press Enter to continue   ")
        
        
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
