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
from social_interaction import *

import time

# NAO's IP address
NAO_IP = "169.254.95.24"

global memory
memory = ALProxy('ALMemory', NAO_IP, 9559)

# Naos sentences:

# Demand for guessing a letter
text_guess_letter = ["Please guess a letter",
                     "Next letter please",
                     "Make a guess",
                     "What's your next letter of choice?"]

# Answer if a guess was right
text_guess_right = ["Your guess was right",
                    "This was correct",
                    "This was right"]

# Answer if a guess was wrong
text_guess_wrong = ["Too bad, this letter is not in the word!",
                    "Your guess was wrong.",
                    "Unfortunately, this was not correct.",
                    "Nice try but no it's not in there."]

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

text_guess_repeated_letter = ["You know that you've guessed this letter before, right?",
                              "You have already guessed this letter before",
                              "You should not guess the same letter twice"]


# NATO alphabet
alphabet = pd.Series.from_csv("nato.csv", header=0)

def main():

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
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # Get Nao's vocabulary
    vocabulary = alphabet.keys().tolist()

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    # Initialze
    greeting()

    # Start the game
    nao_speech(["Okay, let's start with the hang man game"])
    nao_speech(["Let me think about a word"])

    ledsProxy.fadeRGB("FaceLeds", 1 * 1 * 255, 1)
    ledsProxy.fadeRGB("FaceLeds", 1 * 256 * 255, 1)
    ledsProxy.fadeRGB("FaceLeds", 79 * 256 * 255, 1)
    ledsProxy.fadeRGB("FaceLeds", 44 * 1 * 255, 1)
    ledsProxy.fadeRGB("FaceLeds", 226 * 245 * 222, 1)

    nao_speech(["Okay got one"])
    time.sleep(1)

    # Read list of words for hangman  
    dictionary = pd.read_csv("dict_en.txt", sep = '\n').iloc[:, 0].values.tolist()
    
    # Create an instance of a hangman game
    hangman_game = hangman.Hangman(dictionary)


    i = 0  # Counter for while loop
    while True:

        # For example: "Please guess a letter"
        
        # First guess
        if i == 0:
            nao_speech(["Please make your first guess"])
        
        # All successive guesses
        else:
            nao_speech(text_guess_letter)

        # Include if we want to use events instead of a continuous speech recognition
        global SpeechEventListener
        SpeechEventListener = SpeechEventModule("SpeechEventListener", vocabulary)

        # Wait for input
        while True:
            guess_long = memory.getData("WordRecognized")[0]
            if guess_long != '':
                break
            # Check three times per second
            time.sleep(0.33)

        # If something has else been recognized during the set time frame
        if guess_long != '': 

            # Get letter based on NATO word
            guess = alphabet[guess_long]

            # Break on saying stop
            if guess == 'Stop':
                break

            # Repeat letter
            repeat_letter = [sentence + guess for sentence in text_repeat]
            nao_speech(repeat_letter)

            # Determine if letter was in word
            letter_was_in_word = hangman_game.make_guess(guess)

            # Determine status of the letter (0: wrong, 1: right, 2: repeated)
            if letter_was_in_word == 1:
                nao_speech(text_guess_right)

            if letter_was_in_word == 2:
                nao_speech(text_guess_repeated_letter)

            if letter_was_in_word == 0:
                nao_speech(text_guess_wrong)
                               
            hangman_game.print_status()
        
            status = hangman_game.get_status()

            # Determine game status
            if status == 0:
                nao_speech(text_loser)
                winner_move()
                break
            if status == 1:
                nao_speech(text_winner)
                loser_move()
                break
            if status == 2:
                pass
        i += 1

    nao_speech(["This is the end, my friend. Bye bye, H R I people"])
    wave()

if __name__ == "__main__":
    main()
