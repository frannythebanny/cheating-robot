import random

# Note: self.dictionary (or a similiar variable) should be updated, after a guess is made

class Cheaterhangman:

    def __init__(self, dictionary, evil=True):
        self.dictionary = dictionary
        self.evil = evil
        
        self.family = dictionary  
        self.status = ""
        self.guessed_right_letters = set()
        self.guessed_wrong_letters = []


    def initialize(self, word_length):

        """
        Reduce the initial dictionary to words of just a certain length
        """

        self.family = [x for x in self.family if len(x) == word_length]
        self.status = '_' * word_length
        
        return self.family
        
    def create_families(self, guess):
        """
        Take a list of currently possible words and a guess and
        determine the word families 
        """ 
        
        families = {}

        for word in self.family:

            # Determine family, i.e. the visual status of the word, e.g. e__e_
            family = str(self.get_family(word, guess))

            if family in families:
                families[family].add(word)
            else:
                families[family] = set([word])

        print(families)
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

        
    def update_family(self, guess):        

        letter_was_in_word = 0
        
        # Get current families
        families = self.create_families(guess)

        if self.evil:
            # Filter all words that don't have that letter
            sub_families ={family:words for (family,words) in families.iteritems()
                           if guess not in family}

        else:
            # Filter all words that have that letter
            sub_families ={family:words for (family,words) in families.iteritems()
                           if guess in family}

        # Select the largest equivalence class

        if sub_families:
            largestkey = max(sub_families, key=lambda x: len(sub_families[x]))
            largestvalue = sub_families[largestkey]
            print(sub_families[largestkey])
        else:
            largestkey = max(families, key=lambda x: len(families[x]))
            largestvalue = families[largestkey]
            print(families[largestkey])
        
        self.family = largestvalue
        self.status = largestkey
        print(largestvalue)

        # Determine if letter has been guessed before.
        if guess in self.guessed_right_letters or guess in self.guessed_wrong_letters:
            letter_was_in_word = 2
            self.guessed_wrong_letters.append(guess)

        elif guess in largestkey:
            self.guessed_right_letters.add(guess)
            letter_was_in_word = 1            
        else:
            self.guessed_wrong_letters.append(guess)
            letter_was_in_word = 0

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
        elif len(self.guessed_right_letters) == len(list(set(self.status))):
            return 1
        else:
            return 2

    