import random

# Note: self.dictionary (or a similiar variable) should be updated, after a guess is made

class Hangman:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.family = dictionary  # TODO: see if another alternative is better suited
        self.word = self.random_word()
        self.guessed_right_letters = []
        self.guessed_wrong_letters = []

    def random_word(self):
        """ Pick a random word from the dictionary"""

        word = random.choice(self.dictionary).upper()

        print(word)
        return word

    def create_families(self, guess, remaining_words):
        """
        Take a list of currently possible words and a guess and
        determine the word families 
        """ 

        families = {}

        for word in remaining_words:

            # Determine family, i.e. the visual status of the word, e.g. e__e_
            family = str(self.get_family(word, guess))

            if family in families:
                families[family].add(word)
            else:
                families[family] = set([word])

        return families


    def get_family(self, word, guess):
        """
        Determine the visual family of a word, e.g. '_aa_'
        """
        output = []

        for l in word:

            if l in self.guessed_right_letters:
                output.append(l)
            elif l == guess:
                output.append(l)
            else:
                output.append("_")

        status = ''.join(output)
        return status

    def update_family(self, guess, remaining_words):        

        # Get current families
        families = self.create_families(guess, remaining_words)

        # Determine the largest family
        largest = max(families, key=lambda x: len(families[x]))

        self.family = families[largest]
        return families[largest]
    
    def make_guess(self, guess):

        letter_was_in_word = False

        # 'Normalize' word
        guess = guess.upper()

        # Did the player try to solve the word
        if len(guess) > 1:
            if guess == self.word:
                print("You won.")
            else:
                print("Your solution was wrong.")

        else:
            # Todo: catch multiple times the same letter

            if guess in self.word:
                self.guessed_right_letters.append(guess)
                letter_was_in_word = True

            else:
                self.guessed_wrong_letters.append(guess)

        return letter_was_in_word

    def print_status(self, word):

        output = []

        for l in word:

            if l in self.guessed_right_letters:
                output.append(l)
            else:
                output.append("_")

        status = ''.join(output)
        print(status)
        return status


    def get_status(self):

        if len(self.guessed_wrong_letters) == 5:
            return 0
        elif len(self.guessed_right_letters) == len(list(set(self.word))):
            return 1
        else:
            return 2

    