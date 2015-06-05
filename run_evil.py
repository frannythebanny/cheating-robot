import evilhangman
import pandas as pd
import random


def nao_speech(possible_sentences):
    """
    Let Nao randomly select one of the possible sentences and speak them out loud
    """

    print(random.choice(possible_sentences))


dictionary = pd.read_csv("dict_en.txt", sep = '\n').iloc[:, 0].values.tolist()

game = evilhangman.Cheaterhangman(dictionary, False)


print(game.initialize(5))

while True:

    print(game.status)

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

    # Determine game status
    if status == 0:
        print("Loser")
        break
    if status == 1:
        print("Winner")
        break
    if status == 2:
        pass