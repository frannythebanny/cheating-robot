import evilhangman
import pandas as pd
import random
import os
import numpy as np
import requests


def send_status_to_GUI(word_status, guessed_letters, game_status):

    guessed_letters_string = ', '.join(guessed_letters)
    word_status_string = ' '.join(word_status)
    

    print("Updating !!!")
    
    print(guessed_letters_string)

    payload = {
        'word_status': word_status_string,
        'guessed_letters': guessed_letters_string,
        'game_status': game_status
    }

    requests.put("http://195.169.210.194:1234/1", data=payload)


def nao_speech(possible_sentences):
    """
    Let Nao randomly select one of the possible sentences and speak them out loud
    """

    print(random.choice(possible_sentences))


dictionary = pd.read_csv(os.path.join("dictionaries", "nounlist.txt"), sep = '\n').iloc[:, 0].values.tolist()

# game = evilhangman.Cheaterhangman(dictionary, False)
game = evilhangman.Cheaterhangman(dictionary, True)

game.initialize(word_length=6)

while True:


    # Determine initial word

    # I have to update the remaining_words!
    
    guess = raw_input('Please guess a letter: ')

    letter_in_word = game.update_family(guess)

    # Determine status of the letter (0: wrong, 1: right, 2: repeated)
    if letter_in_word == 1:
        nao_speech(["Right"])

    if letter_in_word == 2:
        nao_speech(["Repeated"])

    if letter_in_word == 0:
        nao_speech(["Wrong"])

    game.create_families(guess)

    status = game.get_status()

    # Print current word status, i.e. something like
    # _ _ A _ K _
    print(game.status)

    print(game.guessed_wrong_letters)
    
    # Determine game status
    if status == 0:
        print("Loser")
        print("Word was", random.choice(list(game.family)))
        break
    if status == 1:
        print("Winner")
        break
    if status == 2:
        pass
