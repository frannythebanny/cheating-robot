import hangman
import pandas as pd
import numpy as np

import random

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser
from hangman_speechevent import SpeechEventModule

import time

# Initialize text to Speech
tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
tts.enableNotifications()

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
text_loser = ["Loser",
              "Oh no, you've lost the game",
              "Unfortunately, I have to tell you that you've lost the game",
              "Guess what?! You've lost the game!"]

# Final sentence if the game was won
text_winner = ["Yeah, you've won!",
               "You are the winner!",
               "You won!"]

# Repeat the guess from the user
text_repeat = ["Your guess is: ",
               "You guessed: ",
               "You've chosen letter: ",
               "Your letter is: "]


def nao_speech(possible_sentences):
    """
    Let Nao randomly select one of the possible sentences and speak them out loud
    """

    tts.say("\\bound=S\\\\rspd=75\\" + random.choice(possible_sentences))


# NAO's IP address
NAO_IP = "169.254.95.24"

# Global variables
global SpeechEventListener
SpeechEventListener = None

# Initialize NAO's memory
memory = ALProxy('ALMemory', NAO_IP, 9559)

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
    vocabulary = raw_alphabet.keys().tolist()

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port
    
    
    # Start the game
    nao_speech(["Welcome to my hang man game"])

    # Read list of words for hangman  
    dictionary = pd.read_csv("dict_en.txt", sep = '\n').iloc[:, 0].values.tolist()
    
    # Create an instance of a hangman game
    hangman_game = hangman.Hangman(dictionary)

    while True:

        # For example: "Please guess a letter"
        nao_speech(text_guess_letter)

        # Include if we want to use events instead of a continuous speech recognition
        SpeechEventListener = SpeechEventModule("SpeechEventListener", vocabulary)

        # Wait for input
        while True:
            guess_long = memory.getData("WordRecognized")[0]
            if guess_long != '':
                break
            # Check three times per second
            time.sleep(0.33)

        # Break on saying stop
        if guess_long == 'Stop':
            break

        # If something has else been recognized during the set time frame
        if guess_long != '': 

            # Get letter based on NATO word
            guess = alphabet[guess_long]

            # Repeat letter
            repeat_letter = [sentence + guess for sentence in text_repeat]
            nao_speech(repeat_letter)

            # Determine if letter was in word
            letter_was_in_word = hangman_game.make_guess(guess)

            if letter_was_in_word:
                nao_speech(text_guess_right)

            else:
                nao_speech(text_guess_wrong)
                               
            hangman_game.print_status()
        
            status = hangman_game.get_status()

            # Determine game status
            if status == 0:
                tts.say("\\bound=S\\Loser")
                break
            if status == 1:
                tts.say("\\bound=S\\You won")
                break
            if status == 2:
                pass

if __name__ == "__main__":
    main()
