import hangman
import pandas as pd
import numpy as np
import os

import random
import motion

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser
from hangman_speechevent import SpeechEventModule
import socialInteraction_fran

import time


# Good for debugging because then we can test it without having the nao
NAO_AVAILABLE = True

# NAO's IP address
NAO_IP = "192.168.0.104"  if NAO_AVAILABLE else "localhost"
NAO_PORT = 9559

ledsProxy = ALProxy("ALLeds", NAO_IP, 9559)         

if NAO_AVAILABLE:
    global memory
    memory = ALProxy('ALMemory', NAO_IP, NAO_PORT)

# Naos sentences:

# Demand for guessing a letter
text_guess_letter = ["Please guess a letter",
                     "Next letter please",
                     "Make a guess",
                     "What's your next letter of choice?"]

# Answer if a guess was right
text_guess_right = ["Your guess is right",
                    "This is correct",
                    "This is right"]

# Answer if a guess was wrong
text_guess_wrong = ["Too bad, this letter is not in the word!",
                    "Your guess is wrong.",
                    "Unfortunately, this is not correct.",
                    "Nice try but no, it's not in there."]

# Final sentence if the game was lost
text_loser = ["Loser! Yeah I have won the game!",
              "Oh no, you've lost the game. That means I am the winner!",
              "Unfortunately, I have to tell you that you've lost the game. That means I am the winner!",
              "Guess what?! You've lost the game! And I am the winner!"]

# Final sentence if the game was won
text_winner = ["Yeah, you've won! An I'm the loser",
               "You are the winner! And I lost the game.",
               "Congratulations! You have won the game! That means I'm the loser",
               "You're a hang man professional! You have won! But I lost."]

# Repeat the guess from the user
text_repeat = ["Your guess is: ",
               "You guessed: ",
               "You've chosen letter: ",
               "Your letter is: "]
               
# Ask the user to repeat their letter
ask_repeat = ["Sorry for the misunderstanding. Please repeat your letter.",
               "Could you repeat your letter then?",
               "It would be great if you could repeat your chosen letter again",
               "Which one was your letter then?"]

text_guess_repeated_letter = ["You know that you've guessed this letter before, right?",
                              "You have already guessed this letter before",
                              "You should not guess the same letter twice"]


# NATO alphabet
alphabet = pd.Series.from_csv(os.path.join("dictionaries", "nato.csv"), header=0)
fb_dict = pd.Series.from_csv(os.path.join("dictionaries", "feedback.csv"), header=0)

def main():

    # Get Nao's vocabulary
    vocabulary = alphabet.keys().tolist()
    fb_vocabulary = fb_dict.keys().tolist()

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

    # Initialze
    socialInteraction_fran.greeting(NAO_AVAILABLE)


    # Start the game
    social_interaction.nao_speech(["Okay, let's start with the hang man game"], NAO_AVAILABLE)
    social_interaction.nao_speech(["Let me think about a word"], NAO_AVAILABLE)


    if NAO_AVAILABLE:
        ledsProxy.fadeRGB("FaceLeds", 1 * 1 * 255, 1)
        ledsProxy.fadeRGB("FaceLeds", 1 * 256 * 255, 1)
        ledsProxy.fadeRGB("FaceLeds", 79 * 256 * 255, 1)
        ledsProxy.fadeRGB("FaceLeds", 44 * 1 * 255, 1)
        ledsProxy.fadeRGB("FaceLeds", 226 * 245 * 222, 1)

    social_interaction.nao_speech(["Okay got one"], NAO_AVAILABLE)
    time.sleep(1)

    # Read list of words for hangman  
    dictionary = pd.read_csv(os.path.join("dictionaries", "dict_en.txt"), sep = '\n').iloc[:, 0].values.tolist()
    
    # Create an instance of a hangman game
    hangman_game = hangman.Hangman(dictionary)


    i = 0  # Counter for while loop
    user_canceled = False
    status = 2 # 2 means game is running

    while status == 2:


        print("user_canceled is", user_canceled)

        if i == 0:
            # For example: "Please guess a letter"
            # First guess
            social_interaction.nao_speech(["Please make your first guess"], NAO_AVAILABLE)

        elif user_canceled:
            social_interaction.nao_speech(ask_repeat, NAO_AVAILABLE)
            user_canceled = False

        else:
            social_interaction.nao_speech(text_guess_letter, NAO_AVAILABLE)
        
            
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

        else:
            # Text input
            guess_long = raw_input("DEBUG: Please make a guess (from NATO alphabet):   ")

        # Get letter based on NATO word
        if guess_long in alphabet.index:
            guess = alphabet[guess_long]
        else:
           social_interaction.nao_speech(["This letter is not part of the Nato alphabet"],
                                         NAO_AVAILABLE)
           i += 1
           continue
    

        # Break the entire interaction on saying stop
        # TODO: another safe word would be better
        if guess == 'Stop':
            break

        # Repeat letter
        repeat_letter = [sentence + guess + '?' for sentence in text_repeat]
        social_interaction.nao_speech(repeat_letter, NAO_AVAILABLE)

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
            if feedback == 'No':
                user_canceled = True
                i += 1
                continue


        # THIS IS THE BEGINNING OF THE INTERFACE

        # Determine if the letter was in word
        letter_was_in_word = hangman_game.make_guess(guess)
        
        # END OF INTERFACE

        # Determine status of the letter (0: wrong, 1: right, 2: repeated)
        if letter_was_in_word == 1:
            social_interaction.nao_speech(text_guess_right, NAO_AVAILABLE)

        if letter_was_in_word == 2:
            social_interaction.nao_speech(text_guess_repeated_letter, NAO_AVAILABLE)

        if letter_was_in_word == 0:
            social_interaction.nao_speech(text_guess_wrong, NAO_AVAILABLE)

        hangman_game.print_status()

        status = hangman_game.get_status()

        # Determine game status
        if status == 0:
            social_interaction.nao_speech(text_loser, NAO_AVAILABLE)
            if NAO_AVAILABLE:
                social_interaction.winner_move()
        if status == 1:
            social_interaction.nao_speech(text_winner, NAO_AVAILABLE)
            if NAO_AVAILABLE:
                social_interaction.loser_move()

        i += 1

    
    social_interaction.nao_speech(["This is the end, my friend. Bye bye, H R I people"], NAO_AVAILABLE)

    if NAO_AVAILABLE:
        social_interaction.wave()

if __name__ == "__main__":
    main()
