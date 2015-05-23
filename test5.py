import pandas as pd
import numpy as np
import evilhangman

# Read list of words for hangman  
dictionary = pd.read_csv("dict_en.txt", sep = '\n').iloc[:, 0].values.tolist()

# Create an instance of a hangman game
hangman_game = evilhangman.Hangman(dictionary)

remaining_words = ['abba', 'acca', 'adda', 'efeu', 'dada']

print(hangman_game.create_families('a', remaining_words))



def LargestFamily(families):        
    largest = max(families, key=lambda x: len(families[x]))
    return families[largest]


print LargestFamily(hangman_game.create_families('a', remaining_words))