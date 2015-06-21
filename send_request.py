import requests

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

    requests.put("http://195.169.210.194:1234/1", data=payload)


def send_settings(participant_name, participant_number):

    payload = {
        'participant_name': participant_name,
        'participant_number': participant_number
    }

    requests.put("http://195.169.210.194:1234/settings", data=payload)    
