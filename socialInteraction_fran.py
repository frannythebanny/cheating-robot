import hangman
import pandas as pd
import numpy as np
import os

from global_settings import *

import send_request
import readExcel
import abort

import random
import time
from random import randint

# NAO's IP address
NAO_IP = "192.168.0.104"
#NAO_IP = "10.0.1.5"
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
    
    eos_dict = pd.Series.from_csv(os.path.join("dictionaries", "endofspeech.csv"), header=0)    
    eos_vocabulary = eos_dict.keys().tolist()
    

def nao_speech(possible_sentences, nao_available=True):
    """
    Let Nao randomly select one of the possible sentences and speak them out loud
    """

    text = random.choice(possible_sentences)
    
    if nao_available:
        #tts.say("\\vol=75\\\\vct=85\\\\bound=S\\\\rspd=75\\" + text)
        tts.say("\\bound=S\\\\rspd=85\\" + text)
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
    nao_speech(["Eindelijk iemand die met mij wil spelen \\pau=1000\\"], nao_available)
    

    nao_speech(['Hoi! Ik ben Robin. \\pau=300\\ '], nao_available)

    if nao_available:
        
        handshake()
        
        for i in range(1,4):     
            move_arm_up()
            move_arm_down()
        
        postureProxy.goToPosture("StandInit", 0.7)
    else:
        print('ACTION: nao moves arm up and down four times')
        
    nao_speech(['''en ik ben een robot, maar dat weet je waarschijnlijk al. 
                Ik woon in het ziekenhuis daar'''], nao_available)
              
    if nao_available:
        pointing_closet()
        postureProxy.goToPosture("StandInit", 0.7)
    else: 
        print('ACTION: nao points to closet')
        
    nao_speech(['''of misschien is het eerder \\pau=300\\'''], nao_available)
    
    if nao_available:
        left_arm_point()
    else: 
        print('ACTION: nao points to wall')
        
    nao_speech(['''daar'''], nao_available)
    
    if nao_available:
        #shrug()
        postureProxy.goToPosture("StandInit", 0.7)
    else: 
        print('ACTION: nao shrugs')
        
    nao_speech(['hum ik weet het niet zeker. Robots kunnen ook niet alles weten.'], nao_available)
    
    if nao_available:
        head_right()
    else: 
        print('ACTION: nao looks right')
        
    time.sleep(0.5)
    
    if nao_available:
        head_left()
    else: 
        print('ACTION: nao looks left')
        
    time.sleep(0.3)
    
    if nao_available:
        #shrug()
        postureProxy.goToPosture("StandInit", 0.7)
    else: 
        print('ACTION: nao returns to normal')
    
    
    nao_speech([ '''\\pau=1000\\ Ik vind jullie woning echt leuk! Veel gerieflijker dan het ziekenhuis.\\pau=300\\ 
    Kan je je voorstellen in een ziekenhuis te wonen?  \\pau=700\\'''], nao_available)
                
    if nao_available:

        global SpeechEventListener
        SpeechEventListener = SpeechEventModule("SpeechEventListener", fb_vocabulary)
    
        while True:
            guess_long = SpeechEventListener.memory.getData("WordRecognized")[0]
            if guess_long != '':
                break
                # Check three times per second
            time.sleep(0.33)
            
        SpeechEventListener.unsubscribeFromMemory()
    else:
        # Text input
        raw_input("DEBUG: Can you imagine living in a hospital?")
        
    #Introduction to self-disclosure game
    nao_speech(['''Ook als het niet zo gerieflijk is zijn er wel veel aardige kinderen die dagelijks langs komen, zoals jij!
    Ik ben totaal blij je nu te ontmoeten! Maar eigenlijk vind ik het niet eerlijk, dat ik hier de eenige ben die dingen verteld!
    Ik wil ook graag nog meer van jou weten. Spelen wij een spelletje waar ik jou een kort verhaaltje vertel en dan
    ben jij aan de beurt met een verhaal uit jouw leven. Zo leren wij elkaar nog een beetje beter kennen. Ik ga beginnen.'''],nao_available)
    
    #self-disclosure game with four rounds
    # Demand for guessing a letter
    like_story = ["Wow! Dat was echt een spannend verhaaltje! Nu ben ik weer aan de beurt.",
                  "Ik vind het erg leuk jij zo beter te leren kennen. Nu ben ik weer aan de beurt.",
                  "Interessant! Dat is iets wat ik nog niet wist! Nu ben ik weer aan de beurt."]
                  
    disclosure_list = [readExcel.discDF_lvl0, readExcel.discDF_lvl1, readExcel.discDF_lvl2, readExcel.discDF_lvl3]
        
    if not disclosure_list:
        disclosure_list.append(readExcel.discDF_lvl0)
        disclosure_list.append(readExcel.discDF_lvl1)
        disclosure_list.append(readExcel.discDF_lvl2)
        disclosure_list.append(readExcel.discDF_lvl3)

    i=0
    while i<4:
        say_name_of_child = randint(0,1)
        intimacy_lvl = randint(0,len(disclosure_list)-1)
        intimacy_list = disclosure_list[intimacy_lvl]
        print('This is the intimacy list:' + str(intimacy_lvl))
        del disclosure_list[intimacy_lvl]
        result = readExcel.get_random_disclosure(intimacy_list,'P'+ str(settings['participant_number']))
        disclosure = result[0]
        prompt_id = result[1]
        disclosure = readExcel.parse_content(disclosure, False, name)
        nao_speech(["Laat me even een verhaaltje bedenken. \\pau=2000\\ Okee, ik weet iets. \\pau=500\\"], nao_available)
        nao_speech([disclosure.encode('utf-8')],nao_available)
        
        prompt = readExcel.get_associated_prompt(prompt_id)
        if(say_name_of_child == 1):
            prompt = readExcel.parse_content(prompt, True, name)
        else: prompt = readExcel.parse_content(prompt, False, name)
        nao_speech([prompt.encode('utf-8')], nao_available)
        
        if nao_available:
            # Start to listen to story
            # memory.unsubscribeToEvent("WordRecognized", "SpeechEventListener")                
            global SpeechEventListener3
            SpeechEventListener3 = SpeechEventModule("SpeechEventListener", eos_vocabulary, False)
        
            try:
                while True:
                    guess_long = memory.getData("WordRecognized")[0]
                    confidence = memory.getData("WordRecognized")[1]
                    print(confidence)
                    if (guess_long == "Bitterballen") & (confidence > 0.4):
                        break
                    time.sleep(0.33)
            except KeyboardInterrupt:
                print
                print "Interrupted by user, shutting down"

            SpeechEventListener3.unsubscribeFromMemory()
        
        if i<=1:        
            nao_speech(like_story, nao_available)
        elif i==2: 
            nao_speech(['Laatst \\pau=100\\ rondje, okee? Daarna gaan we galgje spelen! Ik begin weer.'], nao_available)
            
        i = i + 1
        
    readExcel.write_used_disclosures(os.path.join("usedids","used_ids.xlsx"), readExcel.used_disclosures)
    #readExcel.write_used_disclosures("usedids2.xlsx", readExcel.used_disclosures)
    
    nao_speech(['''Vieeuw! Het is leuk maar ook bestwel uitputtend zo veel verhalen te bedenken en te vertellen. 
                Hoe zou je het vinden als wij nu enkele partijtjes galgje gaan spelen? Heb jij daar zin in? '''], nao_available)
                
    if nao_available:
        
        SpeechEventListener = SpeechEventModule("SpeechEventListener", fb_vocabulary)
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
        guess = raw_input("DEBUG: Ja/Nee?:   ")
     
    if guess == 'Ja':
        nao_speech(['Ik ben heel blij dat je met mij wilt spelen! Alleen \\pau=1000\\ ik ben niet de beste galgje speler.'], nao_available)
           
    if nao_available:
        sad()
    else: 
        print('ACTION: nao bows her head to look sad')
    
    if guess == 'Ja':
        nao_speech(['Ik verlies echt vaak.'], nao_available)
    else:
        nao_speech(['''Laten wij het tenminste proberen. Ik hou erg van galgje spelen, en als je het niet leuk vindt kunnen
        wij altijd ermee stoppen. Ik ben ook geen goede speler, ik verlies echt vaak.'''], nao_available)
    
    if nao_available:
        postureProxy.goToPosture("StandInit", 0.7)
        
    nao_speech(['''Maar eigenlijk geeft het niet of men verliest of wint! Ik vind het zo leuk om met kinderen te spelen. 
    Mensen zijn grappig. \\pau=700\\ Mag ik je een geheim vertellen?'''], nao_available)
    
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
        guess = raw_input("DEBUG: Ja/Nee?:   ")
    
    if guess == 'Ja':
        nao_speech(['''Okee, maar je moet een beetje dichter bij komen.\\vol=65\\
        Toen ik met onderzoekers werk val ik soms achterover om ze een beetje te verschrikken. 
        \\pau=500\\ Haha! \\pau=300\\ Je zou eens hun gezichten moeten zien toen het gebeurt. 
        Echt hilarisch.\\pau=1000\\ \\vol=100\\ Oh! Ik vind je heel lief, ''' + name +
        '''. Wij zullen veel lol hebben tijdens het spelletje. Ken je galgje al?'''],nao_available)
            
    else:
        nao_speech(['''Okee, dan hou ik het geheim en vertel je in plaats daarvan een mop. \\pau=700\\ 
        Wat staat er op het graf van een robot? \\pau=3000\\ Roest in vrede! \\pau=500\\ Haha! \\pau = 500\\ Oh! 
        Ik vind je heel aardig ''' + name +
        ''' Wij zullen veel lol hebben tijdens het spelletje. Ken je galgje al?'''],nao_available)
            
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
        guess = raw_input("DEBUG: Ja/Nee?:   ")        
        
    if guess == 'Ja':
            nao_speech(['''Fantastisch! Het eenige verschil 
            deze keer, is dat je alleen letters mag raden en geen hele woorden. Als je een letter wilt 
            zeggen, gebruik dan de woorden op het spiekbriefje. Jouw pogingen en het
            galgje mannetje zullen op het tablet aangetoond worden.'''], nao_available)
            if nao_available:
                pointing_to_phone()
                postureProxy.goToPosture("StandInit", 0.7)
            else: 
                print('ACTION: nao points to phone')
            nao_speech(['Heb je alles begrepen?'],nao_available)              
    else:
        nao_speech(['''Het is helemaal niet moeilijk.
        Ik bedenk een woord en dan teken ik een streep voor iedere letter in het woord op
        dit beeldscherm.'''], nao_available)
        if nao_available:
            pointing_to_phone()    
            postureProxy.goToPosture("StandInit", 0.7)
        else: 
            print('ACTION: nao points to phone')
        nao_speech(['''Daarna mag jij een letter van het alfabet raden. Als het 
        niet in mijn gekozen woord zit, teken ik een deel van het galgje mannetje
        aan de rechterkant van het beeldscherm. Als ik alle tien delen van het 
        mannetje getekend heb en jij nog steeds het woord niet weet, heb jij verloren.
        Als jouw gekozen letter in het woord zit, zal ik het op iedere stip 
        schrijven waar het voorkomt. Je mag alleen letters raden en niet hele woorden.
        Als je een letter wilt raden, moet je het alfabet op het spiekbriefje
        ervoor gebruiken. Heb je alles begrepen?'''],nao_available)
    
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
        guess = raw_input("DEBUG: Ja/Nee?:   ")
        
    if guess == 'Ja':
        nao_speech(['''Tof, dan gaan we aan de slag! Ik zal de spel master zijn en 
        jij moet raden. Als je verliest, krijg ik een punt. Als je een woord helemaal heeft geraden
        krijg jij een punt. Maar voordat we kunnen beginnen, ga ik nog even zitten. Het kan wel
        een beetje duren, zo 'n galgje partijtje.'''],nao_available)
        if nao_available:
            postureProxy.goToPosture("Sit", 0.7)
        else: 
            print('Nao sits down')
                
    else:
        nao_speech(['''Als je nog vragen heeft, stel ze aan Franziska. Ik neem ondertussen een korte pauze.'''], nao_available)
        if nao_available:
            postureProxy.goToPosture("Sit", 0.7)
        else: 
            print('Nao sits down')
        raw_input("Press Enter to continue   ")
        
        
    nao_speech(['Okee, \\pau=500\\ ben je klaar?'], nao_available),

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
                
            abort.abort_speechinput()
    else:
        guess = raw_input('DEBUG: Ja/Nee?:   ')
        
    if guess == 'No':
        nao_speech(['''Als je nog vragen heeft, stel ze aan Franziska. Ik neem ondertussen een korte pauze.'''], nao_available)
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
      #motion = ALProxy("ALMotion", IP, 9559)
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
    
def left_arm_point():
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 0.04000])
    keys.append([ [ 0.05518, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("HeadYaw")
    times.append([ 0.04000])
    keys.append([ [ 0.02143, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnklePitch")
    times.append([ 0.04000])
    keys.append([ [ -0.34979, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnkleRoll")
    times.append([ 0.04000])
    keys.append([ [ 0.00004, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowRoll")
    times.append([ 0.04000])
    keys.append([ [ -0.99246, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 0.04000])
    keys.append([ [ -1.37451, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHand")
    times.append([ 0.04000])
    keys.append([ [ 0.00450, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipPitch")
    times.append([ 0.04000])
    keys.append([ [ -0.45095, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipRoll")
    times.append([ 0.04000])
    keys.append([ [ 0.00004, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipYawPitch")
    times.append([ 0.04000])
    keys.append([ [ 0.00004, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LKneePitch")
    times.append([ 0.04000])
    keys.append([ [ 0.69793, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderPitch")
    times.append([ 0.04000])
    keys.append([ [ 1.44192, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 0.04000])
    keys.append([ [ 0.26227, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 0.04000])
    keys.append([ [ -0.03226, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 0.04000])
    keys.append([ [ -0.34971, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 0.04000])
    keys.append([ [ 0.00004, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 0.04000])
    keys.append([ [ 0.20253, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 0.04000])
    keys.append([ [ 1.46953, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 0.04000])
    keys.append([ [ 0.00636, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipPitch")
    times.append([ 0.04000])
    keys.append([ [ -0.45104, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipRoll")
    times.append([ 0.04000])
    keys.append([ [ 0.00004, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipYawPitch")
    times.append([ 0.04000])
    keys.append([ [ 0.00004, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RKneePitch")
    times.append([ 0.04000])
    keys.append([ [ 0.70415, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderPitch")
    times.append([ 0.04000])
    keys.append([ [ 0.18719, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 0.04000])
    keys.append([ [ -0.57683, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 0.04000])
    keys.append([ [ 0.02757, [ 3, -0.01333, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err

def head_right():
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 0.20000])
    keys.append([ [ 0.03371, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("HeadYaw")
    times.append([ 0.20000])
    keys.append([ [ 0.91422, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnklePitch")
    times.append([ 0.20000])
    keys.append([ [ -0.35133, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnkleRoll")
    times.append([ 0.20000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowRoll")
    times.append([ 0.20000])
    keys.append([ [ -0.99246, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 0.20000])
    keys.append([ [ -1.37451, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHand")
    times.append([ 0.20000])
    keys.append([ [ 0.00441, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipPitch")
    times.append([ 0.20000])
    keys.append([ [ -0.45095, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipRoll")
    times.append([ 0.20000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipYawPitch")
    times.append([ 0.20000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LKneePitch")
    times.append([ 0.20000])
    keys.append([ [ 0.69946, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderPitch")
    times.append([ 0.20000])
    keys.append([ [ 1.43425, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 0.20000])
    keys.append([ [ 0.26227, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 0.20000])
    keys.append([ [ -0.03072, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 0.20000])
    keys.append([ [ -0.35124, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 0.20000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 0.20000])
    keys.append([ [ 0.98794, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 0.20000])
    keys.append([ [ 1.37289, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 0.20000])
    keys.append([ [ 0.00441, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipPitch")
    times.append([ 0.20000])
    keys.append([ [ -0.44950, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipRoll")
    times.append([ 0.20000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipYawPitch")
    times.append([ 0.20000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RKneePitch")
    times.append([ 0.20000])
    keys.append([ [ 0.70108, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderPitch")
    times.append([ 0.20000])
    keys.append([ [ 1.44507, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 0.20000])
    keys.append([ [ -0.27156, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 0.20000])
    keys.append([ [ 0.03677, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err
      
def head_left():
    # Choregraphe bezier export in Python.
    from naoqi import ALProxy
    names = list()
    times = list()
    keys = list()
    
    names.append("HeadPitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.03371, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.00925, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("HeadYaw")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.91422, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.94805, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnklePitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ -0.35133, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.34826, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LAnkleRoll")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowRoll")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ -0.99246, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.99246, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LElbowYaw")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ -1.37451, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -1.37451, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHand")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.00441, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.00445, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipPitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ -0.45095, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.45095, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipRoll")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LHipYawPitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LKneePitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.69946, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.70100, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderPitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 1.43425, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 1.44038, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LShoulderRoll")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.26227, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.26227, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("LWristYaw")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ -0.03072, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.03226, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnklePitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ -0.35124, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.35124, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RAnkleRoll")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowRoll")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.98794, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.98794, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RElbowYaw")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 1.37289, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 1.37289, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHand")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.00441, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.00445, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipPitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ -0.44950, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.44950, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipRoll")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RHipYawPitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.00004, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RKneePitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.70108, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.70568, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderPitch")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 1.44507, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 1.45581, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RShoulderRoll")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ -0.27156, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ -0.27003, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    names.append("RWristYaw")
    times.append([ 0.20000, 0.40000])
    keys.append([ [ 0.03677, [ 3, -0.06667, 0.00000], [ 3, 0.06667, 0.00000]], [ 0.03677, [ 3, -0.06667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion")
      motion.angleInterpolationBezier(names, times, keys);
    except BaseException, err:
      print err

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
