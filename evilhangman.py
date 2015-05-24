import random

# Note: self.dictionary (or a similiar variable) should be updated, after a guess is made

class Evilhangman:

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.family = dictionary  # TODO: see if another alternative is better suited
        self.status = ""
        self.guessed_right_letters = []
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

        # Get current families
        families = self.create_families(guess)

        # Determine the largest family
        largestkey = max(families, key=lambda x: len(families[x]))
        largestvalue = families[largestkey]
        
        self.family = largestvalue
        self.status = largestkey
        print(families[largestkey])
        print(largestvalue)

        if guess in largestkey:
            self.guessed_right_letters.append(guess)
            return True
        else:
            self.guessed_wrong_letters.append(guess)
            return False
            
    
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

    