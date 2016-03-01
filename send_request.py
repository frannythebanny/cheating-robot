import requests
import json
from global_settings import *

def send_status_to_GUI(word_status, wrong_letters, game_status):

    word_status_string = ' '.join(word_status)
    wrong_letters_string = ', '.join(wrong_letters)


    print("Updating !!!")

    print("wrong letters", wrong_letters)
    
    payload = {
        'word_status': word_status_string,
        'wrong_letters': wrong_letters_string,
        'num_wrong_letters': len(wrong_letters),
        'game_status': game_status
    }

    requests.put(server_url + "1", data=payload)


def send_settings(participant_name, game_variant, condition):

    payload = {
        'participant_name': participant_name,  
        'game_variant': game_variant,  # Evil, good, or normal hangman?
        'condition': condition,  # Social or neutral robot?
        'participant_number': 1
    }

    requests.put(server_url + "settings", data=payload)    


def get_settings():

    r = requests.get(server_url + "settings")
    rj = r.json()
    return rj
