import hangman
import pandas as pd
import numpy as np

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

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

# Insert stop command
alphabet['stop'] = 'stop'

print(alphabet)

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
    asr.setVocabulary(vocabulary, False)

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


    # Include if we want to use events instead of a continuous speech recognition
    #global SpeechEventListener
    #SpeechEventListener = SpeechEventModule("SpeechEventListener")

    # Start the game
    
    tts.say("Welcome to our Hangman game")

    dictionary = pd.read_csv("dict_en.txt", sep = '\n').iloc[:, 0].values.tolist()
    hangman_game = hangman.Hangman(dictionary)

    memory = ALProxy('ALMemory', NAO_IP, 9559)

    while True:
        tts.say("Please guess a letter")

        print()

        # Start the speech recognition engine with user Test_ASR
        asr.subscribe("Test_ASR")
        time.sleep(3)
        guess_long = memory.getData("WordRecognized")[0]
        print(memory.getData("WordRecognized"))
        asr.unsubscribe("Test_ASR")

        # Break on saying stop
        if guess_long == 'stop':
            break

        # If something has been recognized during the set time frame
        if guess_long != '': 
            guess = alphabet[guess_long]
            tts.say("You guessed the letter: " + guess)

            letter_was_in_word = hangman_game.make_guess(guess)

            if letter_was_in_word:
                tts.say("Your guess was right")

            else:
                tts.say("Your guess was wrong") 
                               
            hangman_game.print_status()
        
        if hangman_game.is_over():
            tts.say("Loser")
            break

if __name__ == "__main__":
    main()
