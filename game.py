import hangman
import pandas as pd
import numpy as np
import os
from global_settings import *
import random
from random import randint
import evilhangman
import abort


import socialInteraction_fran
#import neutralInteraction_fran

import readExcel


import send_request
import time


# Good for debugging because then we can test it without having the nao

game_variant = 0

# NAO's IP address
NAO_IP = "192.168.0.104" if NAO_AVAILABLE else "localhost"
NAO_PORT = 9559

if NAO_AVAILABLE:

    from hangman_speechevent import SpeechEventModule
    from naoqi import ALProxy
    from naoqi import ALBroker
    from naoqi import ALModule
    import motion
    from optparse import OptionParser
    
    global memory
    memory = ALProxy('ALMemory', NAO_IP, NAO_PORT)
    ledsProxy = ALProxy("ALLeds", NAO_IP, NAO_PORT)


# Naos sentences:

# Demand for guessing a letter
text_guess_letter = ["Raad eens een letter, alsteblieft",
                     "De volgende letter, alsteblieft",
                     "Raad maar",
                     "Voor welke letter wil jij nu kiezen?"]

# Answer if a guess was right
text_guess_right = ["Goed gekozen",
                    "Dit is juist",
                    "Is goed!"]

# Answer if a guess was wrong
text_guess_wrong = ["Helaas zit deze letter niet in het woord!",
                    "Dit was geen goede keuze.",
                    "Helaas fout.",
                    "Goed geprobeerd maar nee, deze letter zit er niet in."]

# Final sentence if the game was lost
text_loser = ["Woehoe! Ik heb gewonnen!",
              "Oh nee, jij hebt verloren. Dat betekent dat ik de winnaar ben!",
              "Helaas moet ik je vertellen dat je verloren hebt. Dat betekent dat ik gewonnen heb!",
              "Jij hebt verloren! En ik ben de winnaar!"]

# Final sentence if the game was won
text_winner = ["Woehoe, jij hebt gewonnen! En ik ben de verliezer.",
               "Jij bent de winnaar! En ik heb dit speel verloren.",
               "Gefeliciteerd! Jij hebt het speel gewonnen! Dat betekent dat ik de verliezer ben.",
               "Jij bent een professionele galgje speler, toch? Jij hebt gewonnen! Ik helaas niet."]

# Repeat the guess from the user
text_repeat = ["Jouw keuze is: ",
               "Jij hebt deze letter geraden: ",
               "Jij hebt voor deze letter gekozen: ",
               "Jouw letter is: "]
               
# Ask the user to repeat their letter
ask_repeat = ["Sorry dat ik het niet begreep. Herhaal jouw keuze alsteblieft?",
               "Kun jij de letter herhalen?",
               "Het zou fantastisch zijn als je de letter opnieuw zegd!",
               "Sorry. Welke letter was het dan?"]

text_guess_repeated_letter = ["Je weet dat je deze letter al geraden heeft, toch?",
                              "Die heb je al geraden!",
                              "Je dient dezelfde letter niet te herhalen!"]


# Children alphabet
alphabet = pd.Series.from_csv(os.path.join("dictionaries", "dutch_children_letters.csv"), header=0)
fb_dict = pd.Series.from_csv(os.path.join("dictionaries", "feedback.csv"), header=0)

def main():

    # Get Nao's vocabulary
    vocabulary = alphabet.keys().tolist()
    fb_vocabulary = fb_dict.keys().tolist()

    print NAO_AVAILABLE

    if NAO_AVAILABLE:
        # NAO parser
        parser = OptionParser()
        parser.add_option("--pip",
            help="Parent broker port. The IP address or your robot",
            dest="pip")
        parser.add_option("--pport",
            help="Parent broker port. The port NAOqi is listening to",
            dest="pport",
            type="int")
        parser.set_defaults(
            pip=NAO_IP,
            pport=NAO_PORT)
            
        (opts, args_) = parser.parse_args()
        pip   = opts.pip
        pport = opts.pport

        # We need this broker to be able to construct
        # NAOqi modules and subscribe to other modules
        # The broker must stay alive until the program exists
        myBroker = ALBroker("myBroker",
           "0.0.0.0",   # listen to anyone
           0,           # find a free port and use it
           pip,         # parent broker IP
           pport)       # parent broker port

    # Check if social or not
    settings = send_request.get_settings()
    DO_SOCIAL_INTERACTION = bool(settings['condition'])
    name = str(settings['participant_name'])
        
    # Do the social interaction in the beginning
    if DO_SOCIAL_INTERACTION:
        socialInteraction_fran.greeting(NAO_AVAILABLE)
    elif NAO_AVAILABLE:
        #neutralInteraction_fran.greeting(NAO_AVAILABLE)
        print("skipping neutral interaction")
    else: 
        print('Nao sits down')
        
    settings = send_request.get_settings()
    game_variant = int(settings['game_variant'])
    
    print("game_variant is", game_variant)
        
    disclosure_list = [readExcel.discDF_lvl0, readExcel.discDF_lvl1, readExcel.discDF_lvl2, readExcel.discDF_lvl3]
    socialInteraction_fran.nao_speech(["Okee, laten wij met het galgje spel beginnen!"], NAO_AVAILABLE)
    rounds = 0
    while rounds<4:
        # Start the game
        
        socialInteraction_fran.nao_speech(["Laat me even een woord bedenken."], NAO_AVAILABLE)
    
        if NAO_AVAILABLE:
            ledsProxy.fadeRGB("FaceLeds", 1 * 1 * 255, 1)
            ledsProxy.fadeRGB("FaceLeds", 1 * 256 * 255, 1)
            ledsProxy.fadeRGB("FaceLeds", 79 * 256 * 255, 1)
            ledsProxy.fadeRGB("FaceLeds", 44 * 1 * 255, 1)
            ledsProxy.fadeRGB("FaceLeds", 226 * 245 * 222, 1)
    
        socialInteraction_fran.nao_speech(["Okee ik weet een woord"], NAO_AVAILABLE)
        time.sleep(1)
    
        # Read list of words for hangman  
        dictionary = pd.read_csv(os.path.join("dictionaries", "nounlist.txt"), sep = '\n').iloc[:, 0].values.tolist()
    
        # Update game variant with info from server
        
        intimacy_lvl = randint(0,len(disclosure_list)-1)
        print('This is the intimacy level:' + str(intimacy_lvl))
        intimacy_list = disclosure_list[intimacy_lvl]
        del disclosure_list[intimacy_lvl]
        result = readExcel.get_random_disclosure(intimacy_list,'P'+ str(settings['participant_number']))
        woord = result[2]
        prompt = result[1]
        disclosure = result[0]
        disclosure = readExcel.parse_content(disclosure, False, name)
        prompt = readExcel.parse_content(prompt, True, name)
        
        eos_dict = pd.Series.from_csv(os.path.join("dictionaries", "endofspeech.csv"), header=0)    
        eos_vocabulary = eos_dict.keys().tolist()
        
        # Create an instance of a hangman game
        if game_variant == 0:
            print("Using normal hangman")
            hangman_game = hangman.Hangman(woord, 7, len(woord))
        elif game_variant == 1:
            print("Using evil hangman")
            hangman_game = evilhangman.Cheaterhangman(dictionary, True)
        elif game_variant == 2:
            print("Using good hangman")
            hangman_game = evilhangman.Cheaterhangman(dictionary, False)
    
        i = 0  # Counter for while loop
        user_canceled = False
        status = 2 # 2 means game is running
    
        while status == 2:
            
            print("user_canceled is", user_canceled)
    
            if i == 0:
                # For example: "Please guess a letter"
                # First guess
                socialInteraction_fran.nao_speech(["Maak je eerste keuze en gebruik het spiekbriefje ervoor."], NAO_AVAILABLE)
    
            elif user_canceled:
                socialInteraction_fran.nao_speech(ask_repeat, NAO_AVAILABLE)
                user_canceled = False
    
            else:
                socialInteraction_fran.nao_speech(text_guess_letter, NAO_AVAILABLE)
            
                
            if NAO_AVAILABLE:
                # Include if we want to use events instead of a continuous speech recognition
                global SpeechEventListener
                SpeechEventListener = SpeechEventModule("SpeechEventListener", vocabulary)
    
                # Wait for first input
                while True:
                    guess_long = memory.getData("WordRecognized")[0]
                    if guess_long != '':
                        break
                    # Check three times per second
                    time.sleep(0.33)
                
                SpeechEventListener.unsubscribeFromMemory()
    
            else:
                # Text input
                guess_long = raw_input("DEBUG: Raad een letter (gebruik woorden van het spiekbriefje):   ")
    
            
            print("Guess_long is", guess_long)
    
            # Get letter based on NATO word
            if guess_long in alphabet.index:
                guess = alphabet[guess_long]
            else:
               socialInteraction_fran.nao_speech(["Deze letter is niet deel van het alfabet op jouw briefje."],
                                             NAO_AVAILABLE)
               i += 1
               continue
        
    
            # Repeat letter
            repeat_letter = [sentence + guess + '?' for sentence in text_repeat]
            socialInteraction_fran.nao_speech(repeat_letter, NAO_AVAILABLE)
    
            if NAO_AVAILABLE:
                # Start to listen for confirmation
                # memory.unsubscribeToEvent("WordRecognized", "SpeechEventListener")                
                global SpeechEventListener2
                SpeechEventListener2 = SpeechEventModule("SpeechEventListener", fb_vocabulary)
    
                feedback = None
                for timer in range(10):
                    interrupt = memory.getData("WordRecognized")[0]
                    print(interrupt)
                    if interrupt != '':
                        feedback = fb_dict[interrupt]
                        break
                    # Check three times per second
                    time.sleep(0.33)                    
    
                    # If user wanted to have another letter 
                print("feedback is", feedback)
                if feedback == 'Nee':
                    user_canceled = True
                    i += 1
                    continue
                
                SpeechEventListener2.unsubscribeFromMemory()
                # Break the entire interaction on saying stop
                # TODO: another safe word would be better
                if feedback == 'Stop':
                    break
                
    
            # Determine if letter was in word
    
            # Difference evil / good!
    
            if game_variant == 0:
                letter_was_in_word = hangman_game.make_guess(guess)
            else:
                letter_was_in_word = hangman_game.update_family(guess)
    
            # Determine status of the letter (0: wrong, 1: right, 2: repeated)
            if letter_was_in_word == 1:
                socialInteraction_fran.nao_speech(text_guess_right, NAO_AVAILABLE)
    
            if letter_was_in_word == 2:
                socialInteraction_fran.nao_speech(text_guess_repeated_letter, NAO_AVAILABLE)
    
            if letter_was_in_word == 0:
                socialInteraction_fran.nao_speech(text_guess_wrong, NAO_AVAILABLE)
    
    
            status = hangman_game.get_status()
    
            # Determine game status
            if status == 0:
                socialInteraction_fran.nao_speech(text_loser, NAO_AVAILABLE)
                if NAO_AVAILABLE:
                    socialInteraction_fran.winner_move()
            if status == 1:
                socialInteraction_fran.nao_speech(text_winner, NAO_AVAILABLE)
                if NAO_AVAILABLE:
                    socialInteraction_fran.loser_move()
    
            i += 1
            
        #At the end of a round
            
        socialInteraction_fran.nao_speech(["Hum, het woord was " + woord.encode('utf-8') + ". Nu schiet me nog een verhaaltje te binnen."], NAO_AVAILABLE)
            
        socialInteraction_fran.nao_speech([disclosure.encode('utf-8')], NAO_AVAILABLE)
        
        prompt_text = readExcel.get_associated_prompt(prompt)
            
        socialInteraction_fran.nao_speech([readExcel.parse_content(prompt_text, True, name).encode('utf-8')], NAO_AVAILABLE)
        
        if NAO_AVAILABLE:
            # Start to listen for confirmation
            # memory.unsubscribeToEvent("WordRecognized", "SpeechEventListener")                
            global SpeechEventListener5
            SpeechEventListener5 = SpeechEventModule("SpeechEventListener", fb_vocabulary)
            
            while True:
                guess_long = SpeechEventListener.memory.getData("WordRecognized")[0]
                if guess_long != '':
                    break
                time.sleep(0.33)  
                
            SpeechEventListene5.unsubscribeFromMemory()
        
            if guess_long in fb_dict.index:
                feedback = fb_dict[guess_long]
            
        else:
            # Text input
            feedback = raw_input("DEBUG: Ja/Nee?:   ")
  
        
        like_story = ["Wow! Dat was echt een spannend verhaaltje!",
                  "Ik vind het erg leuk jij zo beter te leren kennen.",
                  "Interessant! Dat wist ik nog niet!"]
            
        if NAO_AVAILABLE:
            
            if feedback == "Ja":
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
                socialInteraction_fran.nao_speech(like_story, NAO_AVAILABLE)
                
            if feedback == "Nee":
                socialInteraction_fran.nao_speech(["Okee, geeft niet. \\pau=300\\"], NAO_AVAILABLE)
            
        print("will now restart the whole game loop. If child agrees.")
            
        socialInteraction_fran.nao_speech(["Wil jij nog een partijtje spelen?"], NAO_AVAILABLE)
        
        if NAO_AVAILABLE:
            
            global SpeechEventListener4
            SpeechEventListener4 = SpeechEventModule("SpeechEventListener", fb_vocabulary)
            
            # Wait for first input
            while True:
                guess_long = SpeechEventListener4.memory.getData("WordRecognized")[0]
                if guess_long != '':
                    break
                time.sleep(0.33)  
        
            if guess_long in fb_dict.index:
                guess = fb_dict[guess_long]
                
            SpeechEventListener4.unsubscribeFromMemory()
                
        else:
            # Text input
            guess = raw_input("DEBUG: Ja/Nee?:   ")
         
        if guess == 'Ja':
            socialInteraction_fran.nao_speech(['Tof!'], NAO_AVAILABLE)
            rounds += 1
        elif guess == 'Nee':
            socialInteraction_fran.nao_speech(['Jammer, maar ok, dan gaan we iets anders doen!'], NAO_AVAILABLE)
            rounds = 4    
    
    socialInteraction_fran.nao_speech(["Ik vond het ontzettend leuk met je te spelen! Dat moeten we echt eens herhalen!"], NAO_AVAILABLE)
    abort.abort_speechinput
    
    if NAO_AVAILABLE:
        socialInteraction_fran.wave()

if __name__ == "__main__":
    main()
