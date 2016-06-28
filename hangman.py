import random
import send_request

class Hangman:

    def __init__(self, dictionary, max_guesses=7, word_length=6):
        self.dictionary = dictionary
        self.word = self.random_word()
        self.max_guesses = max_guesses
        
        self.guessed_right_letters = set()
        self.guessed_wrong_letters = []
        self.status = self.print_status()
        self.word_length = word_length

        # Send word status to GUI
        send_request.send_status_to_GUI(self.status,
                                        self.guessed_wrong_letters,
                                        self.get_status())


    def random_word(self):
        """ Pick a random word from the dictionary"""

        word = random.choice(self.dictionary).upper()

        print(word)
        return word

    def make_guess(self, guess):

        # 0: wrong
        # 1: right
        # 2: already guessed before
        letter_was_in_word = 0

        # 'Normalize' word
        guess = guess.upper()

        # Did the player try to solve the word
        if len(guess) > 1:
            if guess == self.word:
                print("Jij heeft gewonnen.")
            else:
                print("Jouw poging was fout.")

        else:

            # Determine if letter has been guessed before.
            if guess in self.guessed_right_letters or guess in self.guessed_wrong_letters:
                letter_was_in_word = 2
                self.guessed_wrong_letters.append(guess)


            elif guess in self.word:
                self.guessed_right_letters.add(guess)
                letter_was_in_word = 1

            else:
                self.guessed_wrong_letters.append(guess)
                
        self.status = self.print_status()

        word_status = self.get_status()
        
        # Send word status to GUI
        send_request.send_status_to_GUI(self.status,
                           self.guessed_wrong_letters,
                                        word_status)


        return letter_was_in_word

    def print_status(self):

        output = []

        for l in self.word:

            if l in self.guessed_right_letters:
                output.append(l)
            else:
                output.append("_")
        

        print(''.join(output))
        return ''.join(output)

    def get_status(self):

        if len(self.guessed_wrong_letters) == self.max_guesses:
            self.status = self.word
            return 0
        elif len(self.guessed_right_letters) == len(list(set(self.word))):
            return 1
        else:
            return 2

    
