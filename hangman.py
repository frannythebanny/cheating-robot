import random


class Hangman:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.word = self.random_word()
        self.guessed_right_letters = []
        self.guessed_wrong_letters = []

    def random_word(self):
        """ Pick a random word from the dictionary"""

        word = random.choice(self.dictionary).upper()

        print(word)
        return word

    def make_guess(self, guess):

        letter_was_in_word = False

        # 'Normalize' word
        guess = guess.upper()

        # Did the player try to solve the word
        if len(guess) > 1:
            if guess == self.word:
                print("Winning")

            else:
                print("Wrong!!!")

        else:
            # Todo: catch multiple times the same letter

            if guess in self.word:
                self.guessed_right_letters.append(guess)
                letter_was_in_word = True

            else:
                self.guessed_wrong_letters.append(guess)

        # Check for winning
        if all(l in self.guessed_right_letters for l in self.word):
            print("Winning")

        return letter_was_in_word

    def print_status(self):

        output = []

        for l in self.word:

            if l in self.guessed_right_letters:
                output.append(l)
            else:
                output.append("_")

        print(''.join(output))

    def is_over(self):
        return len(self.guessed_right_letters +
                   self.guessed_wrong_letters) == 10

    