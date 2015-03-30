import hangman


def main():

    dictionary = ['hello', 'little', 'robot']
    hangman_game = hangman.Hangman(dictionary)

    while True:
        guess = raw_input("Please guess a letter (or type your proposed solution): ")
        hangman_game.make_guess(guess)

        hangman_game.print_status()

        if hangman_game.is_over():
            print("Loser")
            break

if __name__ == "__main__":
    main()
