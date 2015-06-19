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