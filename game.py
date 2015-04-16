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


NAO_IP = "169.254.95.24"

# Global variable to store the HumanGreeter module instance
SpeechEventListener = None
memory = None


# NATO alphabet
raw_alphabet = pd.read_csv("nato.txt", sep = '\t')
raw_alphabet.set_index(raw_alphabet.Word)

alphabet = {}
for ix, row in raw_alphabet.iterrows():
    print(row)
    alphabet[row['Word']] = row['Letter']

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

    # Automatic speech recognition
    asr = ALProxy("ALSpeechRecognition", NAO_IP, 9559)
    asr.setLanguage("English")
    
    vocabulary = raw_alphabet.Word.values.tolist()
    # asr.setVocabulary(vocabulary, False)

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port
    

    # Text to Speech
    tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
    tts.enableNotifications()
    # Start the game
    
    tts.say("\\bound=S\\\\rspd=75\\Welcome to our Hang man game")

    dictionary = pd.read_csv("dict_en.txt", sep = '\n').iloc[:, 0].values.tolist()
    hangman_game = hangman.Hangman(dictionary)

    memory = ALProxy('ALMemory', NAO_IP, 9559)

    global SpeechEventListener

    while True:

        text_guess_letter = ["Please guess a letter",
                             "Next letter please",
                             "Make a guess",
                             "What's your next letter of choice?"]

        tts.say("\\bound=S\\\\rspd=75\\" + text_guess_letter[random.randint(0, len(text_guess_letter) - 1)])

        # Include if we want to use events instead of a continuous speech recognition
        SpeechEventListener = SpeechEventModule("SpeechEventListener", vocabulary)

        while True:
            guess_long = memory.getData("WordRecognized")[0]
            if guess_long != '':
                break

        # Break on saying stop
        if guess_long == 'Stop':
            break

        # If something has been recognized during the set time frame
        if guess_long != '': 
            guess = alphabet[guess_long]
            tts.say("You guessed the letter: " + guess)

            letter_was_in_word = hangman_game.make_guess(guess)

            if letter_was_in_word:
                tts.say("\\bound=S\\Your guess was right")

            else:
                tts.say("\\bound=S\\Your guess was wrong") 
                               
            hangman_game.print_status()
        
            status = hangman_game.get_status()

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
